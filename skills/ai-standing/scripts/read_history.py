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
    return str(content)

def clean_user(t):
    t = t.strip()
    # strip Claude Code's injected system reminders / command wrappers
    t = re.sub(r"<system-reminder>.*?</system-reminder>", "", t, flags=re.S)
    t = re.sub(r"<command-[a-z]+>.*?</command-[a-z]+>", "", t, flags=re.S)
    t = re.sub(r"<local-command-[a-z]+>.*?</local-command-[a-z]+>", "", t, flags=re.S)
    return t.strip()[:MAX_USER_CHARS]

# ---------- readers: each yields dict(title, source, started, messages=[{who,text,when}]) ----------

def read_claude_code(root: Path):
    for f in sorted(root.rglob("*.jsonl")):
        msgs, tools, model = [], collections.Counter(), None
        with open(f, errors="ignore") as fh:
            for line in fh:
                try: d = json.loads(line)
                except Exception: continue
                t = d.get("type")
                if t not in ("user", "assistant"): continue
                m = d.get("message") or {}
                content = m.get("content")
                # skip pure tool-result turns (they're plumbing, not the person talking)
                if t == "user" and isinstance(content, list) and content and all(
                    isinstance(p, dict) and p.get("type") == "tool_result" for p in content):
                    continue
                if t == "assistant" and isinstance(content, list):
                    for p in content:
                        if isinstance(p, dict) and p.get("type") == "tool_use":
                            tools[p.get("name", "?")] += 1
                    model = m.get("model") or model
                txt = text_of(content)
                txt = clean_user(txt) if t == "user" else txt.strip()[:ASSIST_PREVIEW]
                if not txt: continue
                msgs.append({"who": "me" if t == "user" else "ai", "text": txt, "when": iso(d.get("timestamp"))})
        if not any(m["who"] == "me" for m in msgs): continue
        first_me = next(m["text"] for m in msgs if m["who"] == "me")
        yield {
            "title": first_me[:80].replace("\n", " "),
            "source": "claude-code",
            "project": f.parent.name,
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

def read_chatgpt(convs):
    for c in convs:
        mapping = c.get("mapping") or {}
        # walk from root, always taking the LAST child (the active branch, usually)
        root = next((k for k, v in mapping.items() if v.get("parent") is None), None)
        msgs, node = [], root
        seen = set()
        while node and node not in seen:
            seen.add(node)
            v = mapping.get(node) or {}
            m = v.get("message")
            if m and m.get("author", {}).get("role") in ("user", "assistant"):
                who = "me" if m["author"]["role"] == "user" else "ai"
                txt = text_of(m.get("content"))
                txt = clean_user(txt) if who == "me" else txt.strip()[:ASSIST_PREVIEW]
                if txt:
                    msgs.append({"who": who, "text": txt, "when": iso(m.get("create_time"))})
            kids = v.get("children") or []
            node = kids[-1] if kids else None
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
    print(f"Dates: {summary['first_chat']} to {summary['last_chat']}. Wrote {out}/summary.json, chats.jsonl, sample.md")

if __name__ == "__main__":
    main()
