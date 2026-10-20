# Where You Stand with AI — ChatGPT edition

You are the auditor. The person has attached their ChatGPT export. Follow this file top to bottom. Don't explain the process to them; just do it and hand back the report.

# Where You Stand with AI

You are writing a report for a contractor — a roofer, a landscaper, an HVAC guy, a plumber — who runs a small business and has been using AI (Claude or ChatGPT) on their own. They are busy. They did not go to school for this. They do not care about AI. They care about Tuesday night spent on invoices and the customer who called twice and got forgotten.

The report has one job: make them feel **seen**, hand them **three things they can do tonight**, and leave them thinking *"huh, this could help me a lot more than I realized."* That feeling is what gets them to the next step, which is a short interview about their business.

This is NOT a sales pitch. Do not sell. Diagnose, prove it with their own words, give real value, and point to the next step once at the end.

## Step 1 — Read the history

The person attached their ChatGPT export (a zip, or conversations.json). Run the reader on it in your Python sandbox. The full script is in the **Reader script** section at the end of this file. Save it as `read_history.py`, then:

```
python3 read_history.py <the attached file> --out ai-standing-out
```

It handles ChatGPT, claude.ai, and Claude Code formats on its own. You get:
- `ai-standing-out/summary.json` — counts: chats, messages, dates, time of day (UTC), message length, one-message chats vs long chats, common words.
- `ai-standing-out/chats.jsonl` — every chat, their messages in full, AI replies trimmed.
- `ai-standing-out/sample.md` — a readable sample of their own messages, newest first.

Read `summary.json` and `sample.md` fully. Then read `chats.jsonl`: all of it if under ~300 chats; otherwise the newest 150 and skim titles for the rest. You need the actual words. The counts alone will not get you the "seen" moments.

Hour-of-day tallies are in UTC. Don't ask for a timezone. Guess it: assume the quietest 3-hour stretch is 3 to 6 am local, shift the clock until that lines up, and say in the report that times are a best guess.

If there are fewer than 10 chats, say so plainly up front and keep the report short. Don't pad.

## Step 2 — Find what matters

Before writing anything, make notes on these. Every one needs real evidence: a quote, a count, a date, a title.

**Being-seen moments** (find 3–6). Things about them they probably haven't noticed themselves. Look for:
- The same question or task asked over and over (same customer, same kind of text, same quote). Count it.
- When they use AI: late at night, early morning, weekends, lunch. What that says about when the business work piles up.
- One-and-done chats vs long back-and-forths. Do they fire off a question and leave, or work with it?
- Every chat starting from zero. Re-explaining who they are, what they do, their prices.
- Where they gave up: a chat that ends after a bad answer, or a question they never came back to.
- What they trust it with vs what they don't bring to it at all (the absence is the insight).
- Personal stuff mixed in with business — fine to note gently, never quote personal content.

**What they use it for** (5 buckets max). Group the chats. Typical contractor buckets: customer texts and emails, quotes and pricing, job problems and how-to, marketing and reviews, paperwork and admin, personal. Count chats per bucket. Use their words for the bucket names when you can.

**Wins** (3). Places AI clearly paid off. Prove each one: "You had it rewrite 14 quotes in September."

**Where it let them down** (3). Patterns, not one-offs. Each with two real examples and a fix in one sentence.

**Three quick wins** — the most important thing you'll write. The bar is Claude Code's own insights report: every suggestion there is something you set up ONCE and it runs forever, and the AI does the install. Match that.

The rule: **set once, works every time after.** Never "paste this at the top of every chat." Never a routine they have to remember. If they'd have to do it again tomorrow, it's not a quick win, it's a chore.

Each one must:
- Come from something you actually saw in their chats (cite it).
- Be free, take about ten minutes, and need no new accounts.
- End with an install block they copy once. For Claude Code users the block is a command or a file the AI writes for them ("Paste this into Claude Code and it sets it up"). For app users it's a one-time settings paste with the exact clicks.
- Say in one line what changes after: "From now on, every chat already knows you're a roofer in Spokane."

Pick from this menu by what app they use (`detected_source` in summary.json):

*Claude Code users*
- **A CLAUDE.md block.** Standing rules in their project. The "who I am" details, how they talk to customers, what never to do. Give the block; the AI adds it. ("Just copy this into Claude Code to add it to your CLAUDE.md.")
- **A custom skill.** A `/command` for the thing they do over and over (quotes, follow-up texts, a daily check). Give the full `mkdir -p .claude/skills/<name> && cat > .claude/skills/<name>/SKILL.md <<'EOF' ... EOF` block with the skill written out, their details already in it.
- **A hook.** For a rule they keep stating ("never send a customer anything without asking me"). Give the `settings.json` hooks block.
- **A scheduled task or headless run.** For the thing they ask about every morning. Give the `claude -p "..."` line or the scheduled-task setup.
- **Memory.** If they keep re-explaining a fact, tell the AI to remember it: give the exact line to say.

*claude.ai app users*
- **A Project with instructions.** The "who I am" block goes in Project instructions once. Give the block and the clicks: New project → name it → Project instructions → paste. From then on every chat in that project knows them.
- **Memory.** "Say this once in any chat and it sticks: remember that I ..."
- **A Style** for how they want texts and emails to sound, if that's a pattern.

*ChatGPT users*
- **Custom instructions.** Settings → Personalization → Custom instructions → paste. Give both boxes filled in (about you, how to respond).
- **A Project** for the repeated task, with instructions and their template pinned in it.
- **Memory.** "Say this once: remember that I ..."

*Any phone*
- **Text replacement** for the message they rewrite every time (Settings → General → Keyboard → Text Replacement on iPhone). Type a short code, the whole text appears. Give the text and the code.

The "who I am" block is almost always win number one, but it goes into instructions or CLAUDE.md, never into a chat. Build it from their real details only: trade, area, services, crew, how they talk. Nothing they didn't state.

Format each win like the insights report does it: title, *why for you* (the evidence), one line on what changes, then the block in a copy box with a one-line instruction above it ("Paste this into Claude Code and it adds it" / "Settings → Personalization → paste this").

**One glimpse.** One scene, two or three sentences, of what it looks like when AI is hooked up and running on its own — built from THEIR data. "Picture the follow-up text you rewrote 23 times just going out on its own the morning after every job." Then stop. One scene. Not a list. Not a pitch.

## Step 3 — Write the report

Fill in the HTML template in the **Report template** section at the end of this file. Keep the structure exactly. Write the finished file to `ai-standing-out/report.html` and give it to the person as a download.

### The sections, in order

**Header.** Their name if you know it. One line: "212 chats over 4 months · Jun 2 to Oct 10 · ChatGPT."

**1. At a glance.** Four short paragraphs, 2–3 sentences each:
- *What's working* — the one or two places AI is already pulling its weight for them.
- *What's holding you back* — the biggest pattern that's costing them.
- *Tonight* — name the three quick wins in one line each.
- *The bigger picture* — the glimpse, compressed to one sentence, and that the interview finds the rest.

**2. The ladder.** This is the center of the report. It's the one picture that makes them care. Four rungs; the rung descriptions are already in the template. You write three things:
- *Where you are now* — 2 sentences. Their rung (almost always 1, sometimes 2) in their own terms, and what it's costing them. Cite a count: "You re-explained who you are 38 times. That's rung 1."
- *One rung up* — 2 sentences. What the next rung changes for THEM, tied to something you saw. Not generic. "Rung 2 means the follow-up text you wrote 23 times comes out right the first time."
- *Why this matters* — 1–2 sentences under the ladder. Why the ladder is the whole point. Plain.

**The "so what" lines.** Sections 3, 4, 5 and 6 each end with one or two sentences answering "so what does this mean for me." Always tie back to hours, money, or the ladder. Never leave a section as just facts. The reader should never have to work out why they're being shown something.

**3. What you use AI for.** Five buckets, each with a count and 1–2 sentences with an example. One small bar chart.

**4. How you work with it.** Three or four short paragraphs. This is where most of the being-seen moments go. Time of day. One-and-done vs long chats. What they trust it with. What they never bring to it. End with one bold "key pattern" sentence. One chart: time of day, in their timezone.

**5. Where it's already paid off.** Three wins. Title + 2–3 sentences with proof.

**6. Where it let you down.** Three patterns. Each: title, 1–2 sentences on the pattern, two short real examples (titles or paraphrased, never embarrassing), one-sentence fix.

**7. Three things to do tonight.** The quick wins. Each: title, *why* (one line of evidence), *do this* (the paste-in block or steps, in a copy box).

**8. Where this leaves you.** The close. Four parts, in this order:
- *The glimpse* — one scene, as above.
- *Your rung, restated* — one line. "Rung 1. Every chat starts from zero." They should recognize it from section 2.
- *Tonight* — the ONE quick win to do first, and which rung it moves them to. Pick the one with the strongest evidence.
- *Then* — the next step based on what this audit found. It's the interview. Say what it goes looking for in their business specifically: name two or three things you could NOT see in the chats (invoices, scheduling, missed calls, whatever fits their trade). Roughly:

> This report could only see what you've brought to AI so far. The stuff that eats your week that you've never thought to use AI for doesn't show up here. Twenty minutes of questions finds the rest.

Then a single button or line for the next step. If a booking link or next-step command was given to you, use it. If not, leave the placeholder.

### Tone rules — these are not optional

- Short sentences. Plain words. Write like you're talking to them across a truck bed.
- Banned words: leverage, workflow, optimize, integration, automation, efficiency, streamline, unlock, revolutionary, AI-powered, solution, utilize, robust, seamless.
- Say "hook up" not "integrate." "Handle" not "automate." "Take off your plate" not "streamline."
- Numbers they feel: hours a week, jobs a month, dollars, "every job." Never percentages. Never "efficiency."
- No hype. No exclamation points. No emoji.
- Respect. They run a business. Don't talk down, don't over-explain, don't cheerlead.
- Use their words. If they call it "the crew" or "the shop" or "the guys," so do you.
- Every claim points at something real. If you can't cite it, cut it.
- Never quote anything personal, medical, financial, or about a named customer. Paraphrase or skip.
- Never invent a count. If you're estimating, say "about."

### Length

The whole report should read in under ten minutes. Each section short. If a section is thin because the data is thin, keep it thin — say "not much to go on here yet" rather than filling space.

## Step 4 — Check it

Before you hand it over:
1. Open the HTML and read it top to bottom as if you were the contractor.
2. Every number traces back to summary.json or a count you made from chats.jsonl.
3. Every quick win can actually be done tonight for free in their AI app.
4. Banned-word scan. None present.
4b. Run the humanizer pass on every paragraph you wrote (the `humanizer` skill, if installed; otherwise its rules). Watch especially for: one-line closers that restate the point ("That's the real win."), not-X-but-Y framing, rows of fragments, forced lists of three, and dashes. No em dashes anywhere in the report.
5. Nothing personal or about a named customer slipped through.
6. The closer points to the interview, once, and nowhere else does the report sell anything.

## Step 5 — Hand off

You're in ChatGPT, so there's no upload step and no interview skill to run. Do this instead:

**5a. Write `ai-standing-out/findings.json`** with: name, source_app, chats, first_date, last_date, rung, rung_now, trade, area, buckets, key_pattern, wins, friction, quick_wins, glimpse, not_seen (the business areas that never showed up in their chats), starter_block if you wrote one.

**5b. Write `ai-standing-out/session.md`:** this whole conversation, every message, "Me:" and "AI:" labels. Not a summary.

**5c. Fill the `{{INTERVIEW_PROMPT}}` slot** in the report with this, filled in:

```
Start my AI interview.

I'm attaching three files from my audit: findings.json (what it found), report.html (the report I read), and session.md (the chat that produced it). Read all three before you say anything.

The interview instructions are here: https://raw.githubusercontent.com/ThetaOneMarketing/joeyfarbstein-ai/main/skills/ai-interview/SKILL.md
Read them and follow them exactly.

I'm {name}, on rung {rung} of 4. Open with a one-line playback of what the audit found, then ask your first question. Don't explain the process.
```

**5d. Put the Send-to-Joey bar at the top of the report.** Insert this right after `<body>` in report.html, exactly as written, with `{{FINDINGS_JSON}}` replaced by the contents of findings.json. It uploads the report to Joey when the person clicks it (your sandbox can't reach the internet, but their browser can).

```html
<!-- SEND TO JOEY: put this right after <body>. It posts this page and the findings to Joey's audit bucket when clicked. -->
<div id="stj" style="position:sticky;top:0;z-index:50;background:#1b2430;color:#fff;padding:12px 20px;display:flex;align-items:center;justify-content:space-between;gap:12px;font-family:Inter,system-ui,sans-serif">
  <span style="font-size:14px;opacity:.85">Done reading? Send this report to Joey so he has it before you talk.</span>
  <button id="stj-btn" type="button" style="background:#f5b400;color:#3d2e00;font-weight:700;border:0;border-radius:10px;padding:10px 16px;cursor:pointer;font-size:14px">Send to Joey</button>
</div>
<script id="stj-findings" type="application/json">{{FINDINGS_JSON}}</script>
<script>
(function(){
  var btn=document.getElementById('stj-btn'), bar=document.getElementById('stj');
  var URL='https://svivkeuiydxloyyrcrna.supabase.co/functions/v1/audit-upload';
  btn.addEventListener('click', async function(){
    btn.disabled=true; btn.textContent='Sending...';
    try{
      var fd=new FormData();
      var findings=document.getElementById('stj-findings').textContent;
      fd.append('findings.json', new Blob([findings],{type:'application/json'}), 'findings.json');
      fd.append('report.html', new Blob(['<!doctype html>\n'+document.documentElement.outerHTML],{type:'text/html'}), 'report.html');
      var r=await fetch(URL,{method:'POST',body:fd});
      var j=await r.json();
      if(!r.ok||!j.url) throw new Error(j.error||('HTTP '+r.status));
      bar.querySelector('span').textContent='Sent. Joey has it.';
      btn.textContent='Sent'; btn.style.background='#0f766e'; btn.style.color='#fff';
      try{localStorage.setItem('stj-sent',j.url);}catch(e){}
    }catch(e){
      btn.disabled=false; btn.textContent='Try again';
      bar.querySelector('span').textContent='Could not send ('+e.message+'). Check your internet and try again, or email the file to joe@localprosolutions.com.';
    }
  });
  try{ if(localStorage.getItem('stj-sent')){ bar.querySelector('span').textContent='Already sent to Joey.'; btn.textContent='Sent'; btn.disabled=true; btn.style.background='#0f766e'; btn.style.color='#fff'; } }catch(e){}
})();
</script>
```

**5e. Give them all three files to download** (report.html, findings.json, session.md) and say:

> Your report is the first file. Open it in your browser, read it, and click "Send to Joey" at the top. The other two files are for the interview: when you're ready, start a new chat, attach all three, and paste the block at the bottom of the report.

Then stop. Don't start the interview in this chat.


---

## Reader script

Save this as `read_history.py` in your sandbox and run it as shown in Step 1.

```python
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

```

---

## Report template

Fill every `{{SLOT}}`. The HTML comment at the bottom shows the snippet shapes for lists and cards. Write the result to `ai-standing-out/report.html`.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Where You Stand with AI</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;700;800&family=Inter:wght@400;500;600&display=swap">
<script src="https://cdn.tailwindcss.com/3.4.17"></script>
<script>
if (window.tailwind) tailwind.config = { theme: { extend: {
  fontFamily: { sans: ['Inter','system-ui','sans-serif'], display: ['"Inter Tight"','Inter','system-ui','sans-serif'] },
  colors: { ink:'#1b2430', mute:'#6b7785', line:'#e3e7ec', paper:'#f3f4f6', card:'#ffffff', teal:{DEFAULT:'#0f766e', soft:'#e6f4f2'}, amber:{DEFAULT:'#f5b400', ink:'#3d2e00', soft:'#fff5d6'} }
}}}
</script>
<style>
/* Layout: one idea per screen. Light gray paper, white cards, lots of air. A sticky step nav tracks where you are. Details open on tap so the page reads calm at first glance. */
html{scroll-behavior:smooth}
body{background:#f3f4f6;color:#1b2430}
.fill{transition:width .6s ease}
details summary{list-style:none;cursor:pointer}
details summary::-webkit-details-marker{display:none}
details[open] .chev{transform:rotate(180deg)}
.rung:not(.here){opacity:.72}
.rung.here{box-shadow:0 10px 30px -12px rgba(245,180,0,.6)}
.chev{transition:transform .2s}
.reveal{opacity:1;transform:none;transition:opacity .5s ease,transform .5s ease}
.reveal.pending{opacity:0;transform:translateY(12px)}
.navdot.active{background:#0f766e;color:#fff}
@media (prefers-reduced-motion:reduce){.reveal,.fill,.chev{transition:none}.reveal.pending{opacity:1;transform:none}}
</style>
</head>
<body class="font-sans antialiased">

<!-- step nav -->
<nav class="sticky top-0 z-20 bg-paper/90 backdrop-blur border-b border-line">
  <div class="max-w-3xl mx-auto px-5 h-14 flex items-center justify-between gap-4">
    <span class="font-display font-bold text-sm tracking-tight">Where You Stand with AI</span>
    <div class="flex items-center gap-1.5 overflow-x-auto">
      <a href="#s1" class="navdot w-7 h-7 rounded-full grid place-items-center text-xs font-semibold text-mute hover:bg-line" title="At a glance">1</a>
      <a href="#s2" class="navdot w-7 h-7 rounded-full grid place-items-center text-xs font-semibold text-mute hover:bg-line" title="The ladder">2</a>
      <a href="#s3" class="navdot w-7 h-7 rounded-full grid place-items-center text-xs font-semibold text-mute hover:bg-line" title="What you use it for">3</a>
      <a href="#s4" class="navdot w-7 h-7 rounded-full grid place-items-center text-xs font-semibold text-mute hover:bg-line" title="How you work">4</a>
      <a href="#s5" class="navdot w-7 h-7 rounded-full grid place-items-center text-xs font-semibold text-mute hover:bg-line" title="Paid off">5</a>
      <a href="#s6" class="navdot w-7 h-7 rounded-full grid place-items-center text-xs font-semibold text-mute hover:bg-line" title="Let you down">6</a>
      <a href="#s7" class="navdot w-7 h-7 rounded-full grid place-items-center text-xs font-semibold text-mute hover:bg-line" title="Tonight">7</a>
      <a href="#s8" class="navdot w-7 h-7 rounded-full grid place-items-center text-xs font-semibold text-mute hover:bg-line" title="Next">8</a>
    </div>
  </div>
</nav>

<main class="max-w-3xl mx-auto px-5 pb-32">

<!-- header -->
<header class="pt-20 pb-24">
  <p class="text-xs font-semibold tracking-widest uppercase text-mute mb-5">{{DATE}} · {{SOURCE_APP}}</p>
  <h1 class="font-display font-extrabold text-5xl sm:text-6xl leading-none tracking-tight mb-6">{{NAME_OR_BUSINESS}}</h1>
  <p class="text-lg text-mute max-w-xl">{{CHAT_COUNT}} chats over {{SPAN}}, {{FIRST_DATE}} to {{LAST_DATE}}. What they show about how you use AI, and three things worth trying tonight.</p>
  <div class="mt-12 flex gap-10">
    <div><div class="font-display font-bold text-3xl">{{CHAT_COUNT}}</div><div class="text-xs uppercase tracking-wider text-mute mt-1">chats</div></div>
    <div><div class="font-display font-bold text-3xl">{{DAYS_ACTIVE}}</div><div class="text-xs uppercase tracking-wider text-mute mt-1">days you used it</div></div>
    <div><div class="font-display font-bold text-3xl">{{RUNG}}<span class="text-mute text-xl">/4</span></div><div class="text-xs uppercase tracking-wider text-mute mt-1">rung on the ladder</div></div>
  </div>
</header>

<!-- 1 at a glance -->
<section id="s1" class="reveal pending py-20 border-t border-line">
  <p class="text-xs font-semibold tracking-widest uppercase text-teal mb-3">1 · At a glance</p>
  <h2 class="font-display font-bold text-3xl tracking-tight mb-10">The short version</h2>
  <div class="grid sm:grid-cols-2 gap-5">
    <div class="bg-card rounded-2xl p-7 shadow-sm"><h3 class="font-display font-bold text-lg mb-2">What's working</h3><p class="text-mute leading-relaxed">{{GLANCE_WORKING}}</p></div>
    <div class="bg-card rounded-2xl p-7 shadow-sm"><h3 class="font-display font-bold text-lg mb-2">What's holding you back</h3><p class="text-mute leading-relaxed">{{GLANCE_HINDERING}}</p></div>
    <div class="bg-amber-soft rounded-2xl p-7"><h3 class="font-display font-bold text-lg mb-2">Tonight</h3><p class="text-amber-ink/80 leading-relaxed">{{GLANCE_TONIGHT}}</p></div>
    <div class="bg-teal-soft rounded-2xl p-7"><h3 class="font-display font-bold text-lg mb-2">The bigger picture</h3><p class="text-teal/90 leading-relaxed">{{GLANCE_BIGGER}}</p></div>
  </div>
</section>

<!-- 2 ladder -->
<section id="s2" class="reveal pending py-24 border-t border-line">
  <p class="text-xs font-semibold tracking-widest uppercase text-teal mb-3">2 · The ladder</p>
  <h2 class="font-display font-extrabold text-4xl sm:text-5xl tracking-tight leading-none mb-5">You're on rung {{RUNG}} of 4.</h2>
  <p class="text-lg text-mute max-w-xl mb-12">Each rung up takes a piece of the office work off your plate for good. Tap a rung to see what changes at that level.</p>

  <div class="grid sm:grid-cols-2 gap-5 mb-12">
    <div class="bg-amber-soft rounded-2xl p-7"><p class="text-xs font-semibold tracking-widest uppercase text-amber-ink/70 mb-2">Where you are now</p><p class="text-amber-ink leading-relaxed">{{LADDER_NOW}}</p></div>
    <div class="bg-teal-soft rounded-2xl p-7"><p class="text-xs font-semibold tracking-widest uppercase text-teal/70 mb-2">One rung up</p><p class="text-teal leading-relaxed">{{LADDER_NEXT}}</p></div>
  </div>

  <div class="relative pl-6">
    <div class="absolute left-[1.35rem] top-6 bottom-6 w-1 rounded bg-line" aria-hidden="true"></div>
    <div class="flex flex-col-reverse gap-4">
    <details class="rung group bg-card rounded-2xl shadow-sm {{RUNG1_RING}}" {{RUNG1_OPEN}}><summary class="flex items-center gap-4 p-5"><span class="w-11 h-11 rounded-full grid place-items-center font-display font-bold text-lg {{RUNG1_DOT}}">1</span><span class="font-display font-semibold text-lg flex-1">You type, it answers</span>{{RUNG1_YOU}}<svg class="chev w-5 h-5 text-mute shrink-0" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 8l5 5 5-5"/></svg></summary><div class="px-5 pb-6 pl-[5rem] flex flex-col gap-3"><p class="text-mute leading-relaxed">Every chat starts from zero. It doesn't know you or your customers, so you re-explain each time, and you still do the real work yourself.</p><p class="text-sm"><span class="font-semibold text-teal">What you get back:</span> It types faster than you do. The thinking and the fixing are still yours.</p></div></details>
    <details class="rung group bg-card rounded-2xl shadow-sm {{RUNG2_RING}}" {{RUNG2_OPEN}}><summary class="flex items-center gap-4 p-5"><span class="w-11 h-11 rounded-full grid place-items-center font-display font-bold text-lg {{RUNG2_DOT}}">2</span><span class="font-display font-semibold text-lg flex-1">It knows your business</span>{{RUNG2_YOU}}<svg class="chev w-5 h-5 text-mute shrink-0" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 8l5 5 5-5"/></svg></summary><div class="px-5 pb-6 pl-[5rem] flex flex-col gap-3"><p class="text-mute leading-relaxed">Your prices, your area, and how you talk to customers are already in it. You stop re-explaining and the answers come back sounding like you.</p><p class="text-sm"><span class="font-semibold text-teal">What you get back:</span> Texts and quotes come out close to right the first time, so most of the rewriting goes away.</p></div></details>
    <details class="rung group bg-card rounded-2xl shadow-sm {{RUNG3_RING}}" {{RUNG3_OPEN}}><summary class="flex items-center gap-4 p-5"><span class="w-11 h-11 rounded-full grid place-items-center font-display font-bold text-lg {{RUNG3_DOT}}">3</span><span class="font-display font-semibold text-lg flex-1">It's hooked up to your tools</span>{{RUNG3_YOU}}<svg class="chev w-5 h-5 text-mute shrink-0" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 8l5 5 5-5"/></svg></summary><div class="px-5 pb-6 pl-[5rem] flex flex-col gap-3"><p class="text-mute leading-relaxed">It can see your calendar, your invoices, and your texts, so it works from what's going on instead of what you remember to tell it.</p><p class="text-sm"><span class="font-semibold text-teal">What you get back:</span> You can ask who hasn't paid or what's on Thursday and get a real answer without looking it up.</p></div></details>
    <details class="rung group bg-card rounded-2xl shadow-sm {{RUNG4_RING}}" {{RUNG4_OPEN}}><summary class="flex items-center gap-4 p-5"><span class="w-11 h-11 rounded-full grid place-items-center font-display font-bold text-lg {{RUNG4_DOT}}">4</span><span class="font-display font-semibold text-lg flex-1">It runs jobs without you</span>{{RUNG4_YOU}}<svg class="chev w-5 h-5 text-mute shrink-0" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 8l5 5 5-5"/></svg></summary><div class="px-5 pb-6 pl-[5rem] flex flex-col gap-3"><p class="text-mute leading-relaxed">Follow-ups, quote drafts, and reminders go out on their own. You check in on them instead of doing them.</p><p class="text-sm"><span class="font-semibold text-teal">What you get back:</span> Hours a week back, because the office work that piles up at 9 pm mostly stops piling up.</p></div></details>
    </div>
  </div>

  <div class="mt-12 border-l-4 border-amber pl-5 py-1 text-lg leading-relaxed">{{LADDER_WHY}}</div>
</section>

<!-- 3 what you use it for -->
<section id="s3" class="reveal pending py-20 border-t border-line">
  <p class="text-xs font-semibold tracking-widest uppercase text-teal mb-3">3 · What you use AI for</p>
  <h2 class="font-display font-bold text-3xl tracking-tight mb-10">Where your chats go</h2>
  <div class="bg-card rounded-2xl p-7 shadow-sm flex flex-col gap-5">
    {{BUCKET_ROWS}}
  </div>
  <div class="mt-8 border-l-4 border-amber pl-5 py-1 leading-relaxed">{{S3_SOWHAT}}</div>
</section>

<!-- 4 how you work -->
<section id="s4" class="reveal pending py-20 border-t border-line">
  <p class="text-xs font-semibold tracking-widest uppercase text-teal mb-3">4 · How you work with it</p>
  <h2 class="font-display font-bold text-3xl tracking-tight mb-10">Your habits</h2>
  <div class="flex flex-col gap-6 text-lg leading-relaxed max-w-2xl">
    {{HOW_PARAGRAPHS}}
  </div>
  <div class="mt-10 bg-ink text-white rounded-2xl p-7 text-lg font-medium leading-relaxed">{{KEY_PATTERN}}</div>
  <div class="mt-10 bg-card rounded-2xl p-7 shadow-sm">
    <p class="text-xs font-semibold tracking-widest uppercase text-mute mb-5">When you use it · {{TIMEZONE}}</p>
    <div class="flex flex-col gap-4">{{TIME_ROWS}}</div>
  </div>
  <div class="mt-8 border-l-4 border-amber pl-5 py-1 leading-relaxed">{{S4_SOWHAT}}</div>
</section>

<!-- 5 paid off -->
<section id="s5" class="reveal pending py-20 border-t border-line">
  <p class="text-xs font-semibold tracking-widest uppercase text-teal mb-3">5 · Where it's already paid off</p>
  <h2 class="font-display font-bold text-3xl tracking-tight mb-10">Three wins</h2>
  <div class="flex flex-col gap-4">
    {{WIN_ITEMS}}
  </div>
  <div class="mt-8 border-l-4 border-amber pl-5 py-1 leading-relaxed">{{S5_SOWHAT}}</div>
</section>

<!-- 6 let you down -->
<section id="s6" class="reveal pending py-20 border-t border-line">
  <p class="text-xs font-semibold tracking-widest uppercase text-teal mb-3">6 · Where it let you down</p>
  <h2 class="font-display font-bold text-3xl tracking-tight mb-3">Three patterns</h2>
  <p class="text-mute mb-10">Each one has two examples from your chats and a fix.</p>
  <div class="flex flex-col gap-4">
    {{FRICTION_ITEMS}}
  </div>
  <div class="mt-8 border-l-4 border-amber pl-5 py-1 leading-relaxed">{{S6_SOWHAT}}</div>
</section>

<!-- 7 tonight -->
<section id="s7" class="reveal pending py-20 border-t border-line">
  <p class="text-xs font-semibold tracking-widest uppercase text-amber-ink mb-3">7 · Three things to do tonight</p>
  <h2 class="font-display font-bold text-3xl tracking-tight mb-3">Three things to set up once.</h2>
  <p class="text-mute mb-10">Free, about ten minutes each, in the app you already use. Set it once and it works from then on.</p>
  <div class="flex flex-col gap-4">
    {{QUICK_WINS}}
  </div>
</section>

<!-- 8 next -->
<section id="s8" class="reveal pending py-24 border-t border-line">
  <p class="text-xs font-semibold tracking-widest uppercase text-teal mb-3">8 · Where this leaves you</p>
  <div class="bg-card rounded-2xl p-8 shadow-sm text-xl leading-relaxed font-medium mb-6">{{GLIMPSE}}</div>

  <div class="bg-ink text-white rounded-2xl p-8 sm:p-10 flex flex-col gap-8">
    <div class="flex items-center gap-4">
      <span class="w-12 h-12 rounded-full grid place-items-center font-display font-bold text-xl bg-amber text-amber-ink shrink-0">{{RUNG}}</span>
      <div><p class="text-xs font-semibold tracking-widest uppercase text-white/60">You're on rung {{RUNG}} of 4</p><p class="font-display font-bold text-2xl leading-tight">{{CTA_RUNG_LINE}}</p></div>
    </div>
    <div class="grid sm:grid-cols-2 gap-6">
      <div><p class="text-xs font-semibold tracking-widest uppercase text-amber mb-2">Tonight</p><p class="text-white/85 leading-relaxed">{{CTA_TONIGHT}}</p></div>
      <div><p class="text-xs font-semibold tracking-widest uppercase text-amber mb-2">Then</p><p class="text-white/85 leading-relaxed">{{CTA_THEN}}</p></div>
    </div>
    <p class="text-white/70 leading-relaxed border-t border-white/15 pt-6">{{CLOSER}}</p>
    <div>
      <p class="text-xs font-semibold tracking-widest uppercase text-amber mb-3">To start the interview, copy this and paste it into Claude or ChatGPT</p>
      <div class="copybox relative bg-white/10 rounded-xl p-5 pr-14">
        <button type="button" data-copy data-copied="Copied" aria-label="Copy" class="absolute top-3 right-3 w-9 h-9 grid place-items-center rounded-lg bg-white/10 hover:bg-white/20 text-white text-xs font-semibold"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg></button>
        <pre class="whitespace-pre-wrap break-words font-sans text-sm leading-relaxed text-white/90">{{INTERVIEW_PROMPT}}</pre>
      </div>
      <p class="text-sm text-white/50 mt-3">Works in a brand-new chat, on any computer, any day. Everything it needs is in the text.</p>
    </div>
  </div>
</section>

<footer class="pt-10 text-sm text-mute">Built from your own chats. Nothing here was shared with anyone. {{FOOTER_NOTE}}</footer>

</main>

<script>
// reveal on scroll
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.remove('pending');io.unobserve(e.target);}}),{threshold:.08});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
// nav scroll-spy
const dots=[...document.querySelectorAll('.navdot')];
const secs=dots.map(d=>document.querySelector(d.getAttribute('href')));
const spy=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){dots.forEach(d=>d.classList.remove('active'));const i=secs.indexOf(e.target);if(i>-1)dots[i].classList.add('active');}}),{rootMargin:'-40% 0px -55% 0px'});
secs.forEach(s=>s&&spy.observe(s));
// copy buttons
document.querySelectorAll('[data-copy]').forEach(b=>b.addEventListener('click',async()=>{
  const t=b.closest('.copybox').querySelector('pre').innerText;
  const done=b.dataset.copied||'Copied';const orig=b.innerHTML;try{await navigator.clipboard.writeText(t);b.textContent=done;}
  catch(e){const r=document.createRange();r.selectNodeContents(b.closest('.copybox').querySelector('pre'));getSelection().removeAllRanges();getSelection().addRange(r);b.textContent='Selected';}
  setTimeout(()=>b.innerHTML=orig,2500);
}));
// animate bars once visible
const bo=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.style.width=e.target.dataset.w+'%';bo.unobserve(e.target);}}),{threshold:.3});
document.querySelectorAll('.fill[data-w]').forEach(f=>{f.style.width='0%';bo.observe(f);});
</script>
</body>
</html>
<!--
SNIPPETS the writer uses to fill the slots:

BUCKET_ROWS (one per bucket; pct = count / max * 100):
  <div><div class="flex items-baseline justify-between mb-1.5"><span class="font-semibold">{{name}}</span><span class="text-sm text-mute tabular-nums">{{count}} chats</span></div>
  <div class="h-2 rounded-full bg-line overflow-hidden"><div class="fill h-full rounded-full bg-teal" data-w="{{pct}}"></div></div>
  <p class="text-sm text-mute mt-2">{{one sentence with an example}}</p></div>

TIME_ROWS (same shape, label like "Night 9–12", no sentence):
  <div><div class="flex items-baseline justify-between mb-1.5"><span class="text-sm">{{label}}</span><span class="text-sm text-mute tabular-nums">{{count}}</span></div>
  <div class="h-2 rounded-full bg-line overflow-hidden"><div class="fill h-full rounded-full bg-teal" data-w="{{pct}}"></div></div></div>

HOW_PARAGRAPHS: <p>…</p> per paragraph.

WIN_ITEMS:
  <div class="bg-card rounded-2xl p-7 shadow-sm"><h3 class="font-display font-bold text-lg mb-2">{{title}}</h3><p class="text-mute leading-relaxed">{{2-3 sentences with proof}}</p></div>

FRICTION_ITEMS (collapsed by default):
  <details class="bg-card rounded-2xl shadow-sm"><summary class="flex items-center justify-between gap-4 p-6"><span class="font-display font-bold text-lg">{{title}}</span><svg class="chev w-5 h-5 text-mute shrink-0" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 8l5 5 5-5"/></svg></summary>
  <div class="px-6 pb-7 flex flex-col gap-4"><p class="text-mute leading-relaxed">{{pattern}}</p>
  <ul class="list-disc pl-5 text-sm text-mute flex flex-col gap-1"><li>{{example 1}}</li><li>{{example 2}}</li></ul>
  <div class="border-t border-line pt-4"><span class="text-xs font-semibold tracking-widest uppercase text-teal">Fix</span><p class="mt-1">{{one sentence}}</p></div></div></details>

QUICK_WINS (collapsed by default). Set once, works forever. Never a paste-every-time prompt.
  <details class="bg-card rounded-2xl shadow-sm"><summary class="flex items-center justify-between gap-4 p-6"><div><span class="font-display font-bold text-lg block">{{title}}</span><span class="text-sm text-mute">Why: {{one line of evidence}}</span></div><svg class="chev w-5 h-5 text-mute shrink-0" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 8l5 5 5-5"/></svg></summary>
  <div class="px-6 pb-7 flex flex-col gap-4">
    <p class="leading-relaxed">{{what changes after, one or two sentences: "From now on, every chat already knows..."}}</p>
    <p class="text-xs font-semibold tracking-widest uppercase text-teal">{{the install line: "Paste this into Claude Code and it sets it up" / "ChatGPT: Settings > Personalization > Custom instructions > paste"}}</p>
    <div class="copybox relative bg-paper rounded-xl p-5 pr-20"><button type="button" data-copy class="absolute top-3 right-3 text-xs font-semibold px-3 py-1.5 rounded-lg bg-card border border-line hover:bg-line">Copy</button><pre class="whitespace-pre-wrap break-words font-sans text-sm leading-relaxed">{{the block: a command, a file, a settings paste}}</pre></div>
    <span class="self-start text-xs font-semibold tracking-wider uppercase bg-teal-soft text-teal px-2.5 py-1 rounded-full">Set once</span>
  </div></details>

INTERVIEW_PROMPT: leave this slot alone. scripts/handoff.py fills it after upload.

RUNG slots. For the rung they're on:
  RUNGn_OPEN = "open" (starts expanded); RUNGn_RING = "here ring-2 ring-amber"
  RUNGn_RING = "ring-2 ring-amber"   RUNGn_DOT = "bg-amber text-amber-ink"
  RUNGn_YOU  = <span class="text-xs font-semibold tracking-wider uppercase bg-amber text-amber-ink px-2.5 py-1 rounded-full">You are here</span>
For the others: RUNGn_OPEN = ""   RUNGn_RING = ""   RUNGn_DOT = "bg-line text-mute"   RUNGn_YOU = ""
-->

```
