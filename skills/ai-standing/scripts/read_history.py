#!/usr/bin/env python3
"""
read_history.py — turn any AI chat history into one simple shape, plus tallies.

Usage:
  python3 read_history.py <path> [--out DIR] [--days N]

<path> can be:
  - a Claude Code projects folder   (~/.claude/projects)
  - a claude.ai export              (conversations.json, or the zip/folder holding it)
  - a ChatGPT export                (conversations.json, or the zip/folder holding it)

Writes to --out (default ./ai-standing-out):
  summary.json   counts and tallies (no AI needed)
  chats.jsonl    one line per chat: title, dates, source, messages [{who, text, when}]
  sample.md      a readable sample of the person's own messages, for the writer

Claude Code folders: scheduled jobs, headless runs (claude -p), subagents and
temp-folder sessions are skipped, and machine messages (task notifications,
shell echoes, skill bodies, "Request interrupted" markers) are not counted as
the person's words. The counts in summary.json say how many were skipped.

ChatGPT exports: only the branch the person actually kept (current_node) is
read, and hidden custom-instructions messages are not counted as theirs.

Only the person's own messages are kept at full length. Assistant replies are
trimmed to a short preview — the report is about how THEY use AI, not what AI said.
"""
import argparse, json, os, re, sys, zipfile, io, collections, datetime as dt
from pathlib import Path

ASSIST_PREVIEW = 300          # chars of each assistant reply we keep
MAX_USER_CHARS = 4000         # cap per user message (keeps giant pastes from swamping)
SAMPLE_CHATS = 60             # how many chats go into sample.md
SAMPLE_USER_MSGS_PER_CHAT = 8

# ---------- helpers ----------

def iso(ts):
    """Accept unix seconds, ms, or ISO string → ISO string (UTC)."""
    if ts is None:
        return None
    try:
        if isinstance(ts, (int, float)):
            if ts > 1e12: ts = ts / 1000
            return dt.datetime.fromtimestamp(ts, dt.timezone.utc).isoformat()
        s = str(ts)
        return dt.datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(dt.timezone.utc).isoformat()
    except Exception:
        return None

def parse_iso(s):
    try:
        return dt.datetime.fromisoformat(s)
    except Exception:
        return None

def text_of(content):
    """Flatten the many content shapes into plain text."""
    if content is None: return ""
    if isinstance(content, str): return content
    if isinstance(content, list):
        out = []
        for part in content:
            if isinstance(part, str): out.append(part)
            elif isinstance(part, dict):
                t = part.get("type")
                if t == "text" and part.get("text"): out.append(part["text"])
                elif t == "tool_use": out.append(f"[used tool: {part.get('name','?')}]")
                elif t == "tool_result": out.append("[tool result]")
                elif part.get("text"): out.append(str(part["text"]))
        return "\n".join(out)
    if isinstance(content, dict):
        if "parts" in content: return text_of(content["parts"])
        if "text" in content: return str(content["text"])
        return ""   # e.g. ChatGPT custom-instructions blocks: not something the person typed
    return str(content)

# Messages that land in the log as "user" but were written by a machine, not the person.
MACHINE_PREFIXES = (
    "<task-notification", "<bash-input>", "<bash-stdout>", "<bash-stderr>",
    "<local-command-stdout>", "<user-prompt-submit-hook>", "<command-message>",
    "[Request interrupted", "Caveat: The messages below were generated",
    "Base directory for this skill:", "This session is being continued from a previous conversation",
)
# First-message markers of a scheduled job or headless run (Claude Code). From the first real run.
HEADLESS_MARKERS = (
    "<scheduled-task", "running headless", "Print exactly", "RESULT: OK", "/insights",
    "You are a subagent", "You are running as a scheduled",
)
# Claude Code project folders that are scratch space, not a person at a keyboard.
TEMP_PROJECT_PREFIXES = ("-private-var-", "-private-tmp", "-tmp", "-var-folders-")
HEADLESS_ENTRYPOINTS = {"sdk-cli", "sdk-ts", "sdk-py", "sdk"}

def is_machine_text(t):
    s = t.lstrip()
    return s.startswith(MACHINE_PREFIXES)

def clean_user(t):
    t = t.strip()
    # strip Claude Code's injected system reminders / command wrappers
    t = re.sub(r"<system-reminder>.*?</system-reminder>", "", t, flags=re.S)
    t = re.sub(r"<command-[a-z]+>.*?</command-[a-z]+>", "", t, flags=re.S)
    t = re.sub(r"<local-command-[a-z]+>.*?</local-command-[a-z]+>", "", t, flags=re.S)
    t = re.sub(r"\[Image #\d+\]", "", t)
    t = t.strip()
    if is_machine_text(t):
        return ""
    return t[:MAX_USER_CHARS]

# ---------- readers: each yields dict(title, source, started, messages=[{who,text,when}]) ----------

SKIPPED = collections.Counter()   # why chats were left out; reported in summary.json

def read_claude_code(root: Path):
    for f in sorted(root.rglob("*.jsonl")):
        rel_parts = f.relative_to(root).parts
        project = f.parent.name
        # subagent transcripts live in a "subagents" folder next to the session; they're the AI talking to itself
        if "subagents" in rel_parts or f.name.startswith("agent-"):
            SKIPPED["subagent"] += 1; continue
        top = rel_parts[0] if len(rel_parts) > 1 else project
        if top.startswith(TEMP_PROJECT_PREFIXES):
            SKIPPED["temp_folder"] += 1; continue
        msgs, tools, model, headless = [], collections.Counter(), None, False
        with open(f, errors="ignore") as fh:
            for line in fh:
                try: d = json.loads(line)
                except Exception: continue
                t = d.get("type")
                if t not in ("user", "assistant"): continue
                if d.get("isSidechain"): continue            # subagent turns inside a session
                if str(d.get("entrypoint") or "") in HEADLESS_ENTRYPOINTS: headless = True
                m = d.get("message") or {}
                content = m.get("content")
                # skip pure tool-result turns (they're plumbing, not the person talking)
                if t == "user" and isinstance(content, list) and content and all(
                    isinstance(p, dict) and p.get("type") == "tool_result" for p in content):
                    continue
                if t == "user" and (d.get("isMeta") or d.get("isCompactSummary")):
                    continue                                   # injected by Claude Code, not typed
                if t == "assistant" and isinstance(content, list):
                    for p in content:
                        if isinstance(p, dict) and p.get("type") == "tool_use":
                            tools[p.get("name", "?")] += 1
                    model = m.get("model") or model
                txt = text_of(content)
                txt = clean_user(txt) if t == "user" else txt.strip()[:ASSIST_PREVIEW]
                if not txt: continue
                msgs.append({"who": "me" if t == "user" else "ai", "text": txt, "when": iso(d.get("timestamp"))})
        if not any(m["who"] == "me" for m in msgs):
            SKIPPED["no_typed_messages"] += 1; continue
        first_me = next(m["text"] for m in msgs if m["who"] == "me")
        if headless:
            SKIPPED["headless_run"] += 1; continue
        if any(k.lower() in first_me[:2000].lower() for k in HEADLESS_MARKERS):
            SKIPPED["scheduled_or_headless"] += 1; continue
        yield {
            "title": first_me[:80].replace("\n", " "),
            "source": "claude-code",
            "project": project,
            "started": next((m["when"] for m in msgs if m["when"]), None),
            "tools": dict(tools),
            "model": model,
            "messages": msgs,
        }

def read_claude_ai(convs):
    for c in convs:
        msgs = []
        for m in c.get("chat_messages", []):
            who = "me" if m.get("sender") == "human" else "ai"
            txt = m.get("text") or text_of(m.get("content"))
            txt = clean_user(txt) if who == "me" else txt.strip()[:ASSIST_PREVIEW]
            if not txt: continue
            msgs.append({"who": who, "text": txt, "when": iso(m.get("created_at"))})
        if not any(m["who"] == "me" for m in msgs): continue
        yield {
            "title": (c.get("name") or msgs[0]["text"][:80]).replace("\n", " "),
            "source": "claude-ai",
            "project": None,
            "started": iso(c.get("created_at")) or next((m["when"] for m in msgs if m["when"]), None),
            "tools": {},
            "model": None,
            "messages": msgs,
        }

def _chatgpt_path(mapping, current):
    """The messages on the branch the person actually kept, root first.
    ChatGPT stores every edit and regenerate as a branch. current_node marks the one on screen;
    walk from it up to the root. Older exports without current_node: walk down taking the last child."""
    if current and current in mapping:
        path, node, seen = [], current, set()
        while node and node not in seen and node in mapping:
            seen.add(node); path.append(node)
            node = mapping[node].get("parent")
        return list(reversed(path))
    root = next((k for k, v in mapping.items() if v.get("parent") is None), None)
    path, node, seen = [], root, set()
    while node and node not in seen:
        seen.add(node); path.append(node)
        kids = (mapping.get(node) or {}).get("children") or []
        node = kids[-1] if kids else None
    return path

def read_chatgpt(convs):
    for c in convs:
        mapping = c.get("mapping") or {}
        msgs = []
        for node in _chatgpt_path(mapping, c.get("current_node")):
            m = (mapping.get(node) or {}).get("message")
            if not m or m.get("author", {}).get("role") not in ("user", "assistant"): continue
            meta = m.get("metadata") or {}
            ctype = (m.get("content") or {}).get("content_type")
            # custom instructions and other hidden context ride along as "user" messages; they aren't typed
            if meta.get("is_visually_hidden_from_conversation") or ctype in ("user_editable_context", "model_editable_context"):
                continue
            who = "me" if m["author"]["role"] == "user" else "ai"
            txt = text_of(m.get("content"))
            txt = clean_user(txt) if who == "me" else txt.strip()[:ASSIST_PREVIEW]
            if txt:
                msgs.append({"who": who, "text": txt, "when": iso(m.get("create_time"))})
        if not any(m["who"] == "me" for m in msgs): continue
        yield {
            "title": (c.get("title") or msgs[0]["text"][:80]).replace("\n", " "),
            "source": "chatgpt",
            "project": None,
            "started": iso(c.get("create_time")) or next((m["when"] for m in msgs if m["when"]), None),
            "tools": {},
            "model": None,
            "messages": msgs,
        }

# ---------- detect + load ----------

def load_json_from(path: Path):
    """Find conversations.json inside a file, folder, or zip."""
    if path.is_file() and path.suffix == ".zip":
        with zipfile.ZipFile(path) as z:
            name = next((n for n in z.namelist() if n.endswith("conversations.json")), None)
            if not name: sys.exit("No conversations.json inside that zip.")
            return json.load(io.TextIOWrapper(z.open(name), encoding="utf-8"))
    if path.is_file():
        return json.load(open(path, encoding="utf-8"))
    cand = next(path.rglob("conversations.json"), None)
    if cand: return json.load(open(cand, encoding="utf-8"))
    return None

def detect_and_read(path: Path):
    if path.is_dir() and any(path.rglob("*.jsonl")):
        return "claude-code", list(read_claude_code(path))
    data = load_json_from(path)
    if data is None: sys.exit(f"Couldn't find chat history at {path}")
    if isinstance(data, list) and data:
        first = data[0]
        if "chat_messages" in first: return "claude-ai", list(read_claude_ai(data))
        if "mapping" in first:       return "chatgpt",   list(read_chatgpt(data))
    sys.exit("Found a JSON file but didn't recognize the format.")

# ---------- tallies ----------

def tally(chats):
    me = [m for c in chats for m in c["messages"] if m["who"] == "me"]
    whens = [parse_iso(m["when"]) for m in me if m["when"]]
    whens = [w for w in whens if w]
    hours = collections.Counter(w.hour for w in whens)  # UTC; the writer converts if a timezone is known
    weekdays = collections.Counter(w.strftime("%A") for w in whens)
    lengths = [len(m["text"]) for m in me]
    lengths_sorted = sorted(lengths)
    med = lengths_sorted[len(lengths_sorted)//2] if lengths_sorted else 0
    per_chat = [sum(1 for m in c["messages"] if m["who"] == "me") for c in chats]
    one_and_done = sum(1 for n in per_chat if n == 1)
    long_chats = sum(1 for n in per_chat if n >= 8)
    tools = collections.Counter()
    for c in chats: tools.update(c.get("tools") or {})
    # crude topic words from titles + first messages
    words = collections.Counter()
    stop = set("the a an and or to of in on for with is it this that i my me you your we our at by be as from how what can do about up".split())
    for c in chats:
        for w in re.findall(r"[a-zA-Z]{4,}", (c["title"] + " " + c["messages"][0]["text"]).lower()):
            if w not in stop: words[w] += 1
    span = sorted(w for w in whens)
    by_month = collections.defaultdict(collections.Counter)
    for w in whens: by_month[w.strftime("%Y-%m")][w.hour] += 1
    peak_by_month = {k: v.most_common(1)[0][0] for k, v in sorted(by_month.items())}
    peaks = list(peak_by_month.values())
    shift = any(abs(a - b) % 24 >= 5 and abs(a - b) % 24 <= 19 for a, b in zip(peaks, peaks[1:]))
    return {
        "chats": len(chats),
        "my_messages": len(me),
        "first_chat": span[0].date().isoformat() if span else None,
        "last_chat": span[-1].date().isoformat() if span else None,
        "days_active": len({w.date() for w in whens}),
        "median_message_chars": med,
        "one_message_chats": one_and_done,
        "long_chats_8plus": long_chats,
        "messages_per_chat_avg": round(len(me)/len(chats), 1) if chats else 0,
        "hour_of_day_utc": dict(sorted(hours.items())),
        "weekday": dict(weekdays),
        "tools_used": dict(tools.most_common(15)),
        "common_words": dict(words.most_common(40)),
        "sources": dict(collections.Counter(c["source"] for c in chats)),
        "busiest_hour_utc_by_month": peak_by_month,
        "possible_timezone_change": shift,
        "skipped_not_typed_by_person": dict(SKIPPED),
    }

def write_sample(chats, out: Path):
    chats_sorted = sorted(chats, key=lambda c: c["started"] or "", reverse=True)[:SAMPLE_CHATS]
    with open(out / "sample.md", "w") as f:
        f.write("# Sample of the person's own messages (newest first)\n\n")
        for c in chats_sorted:
            f.write(f"## {c['title']}  \n*{(c['started'] or '')[:10]} · {c['source']}*\n\n")
            n = 0
            for m in c["messages"]:
                if m["who"] != "me": continue
                f.write(f"- {m['text'][:600].strip()}\n")
                n += 1
                if n >= SAMPLE_USER_MSGS_PER_CHAT: break
            f.write("\n")

# ---------- main ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--out", default="ai-standing-out")
    ap.add_argument("--days", type=int, default=0, help="only keep chats from the last N days (0 = all)")
    a = ap.parse_args()
    src, chats = detect_and_read(Path(a.path).expanduser())
    if a.days:
        cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=a.days)
        chats = [c for c in chats if c["started"] and parse_iso(c["started"]) and parse_iso(c["started"]) >= cutoff]
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    with open(out / "chats.jsonl", "w") as f:
        for c in chats: f.write(json.dumps(c) + "\n")
    summary = tally(chats); summary["detected_source"] = src
    json.dump(summary, open(out / "summary.json", "w"), indent=2)
    write_sample(chats, out)
    print(f"Read {summary['chats']} chats ({summary['my_messages']} of your messages) from {src}.")
    if SKIPPED:
        print(f"Skipped {sum(SKIPPED.values())} sessions that weren't the person typing: {dict(SKIPPED)}")
    if summary["possible_timezone_change"]:
        print("Heads up: the busiest hour moves a lot between months. The person may have changed timezones.")
    print(f"Dates: {summary['first_chat']} to {summary['last_chat']}. Wrote {out}/summary.json, chats.jsonl, sample.md")

if __name__ == "__main__":
    main()
