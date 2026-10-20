#!/usr/bin/env python3
"""Rebuild every generated file from its source. Run from anywhere:  python3 chatgpt/build_pack.py

What it does, in order:
  1. Reads BOOKING_URL from config.json and stamps it into every page and snippet that has a
     "Book a call with Joey" button (the line  var BOOKING_URL="...";).
  2. Builds chatgpt/quick-look-prompt.md and claude-app/quick-look-prompt.md from
     shared/quick-look.src.md, with the Send-to-Joey snippet pasted in.
  3. Refreshes the three embedded blocks in chatgpt/audit-pack.md: the Send-to-Joey snippet,
     the reader script, and the report template. The prose in audit-pack.md is edited by hand.
  4. Rebuilds sample-opportunities.html from examples/example-profile.json.

Edit the sources (config.json, shared/, skills/, chatgpt/send-to-joey-snippet.html), never the outputs.
"""
import json, pathlib, re, subprocess, sys
sys.stdout.reconfigure(line_buffering=True)

root = pathlib.Path(__file__).resolve().parent.parent
R = lambda p: (root / p).read_text()
def W(p, s):
    path = root / p
    if not path.exists() or path.read_text() != s:
        path.write_text(s); print(f"  wrote {p}")
    else:
        print(f"  unchanged {p}")

# 1. booking link -------------------------------------------------------------
booking = json.loads(R("config.json"))["BOOKING_URL"].strip()
if '"' in booking or "\\" in booking:
    sys.exit("BOOKING_URL in config.json can't contain quotes or backslashes.")
BOOKING_RE = re.compile(r'(var BOOKING_URL\s*=\s*")[^"]*(")')
for p in ["chatgpt/send-to-joey-snippet.html",
          "skills/ai-standing/templates/report.html",
          "skills/ai-interview/templates/opportunities.html",
          "sample-report.html",
          "skills/ai-interview/SKILL.md"]:
    s = R(p)
    if not BOOKING_RE.search(s):
        sys.exit(f"{p} has no  var BOOKING_URL=\"...\";  line. Put it back before building.")
    W(p, BOOKING_RE.sub(lambda m: m.group(1) + booking + m.group(2), s))
print(f"Booking link: {booking if booking.startswith('http') else 'not set yet (buttons email Joey instead)'}")

snippet = R("chatgpt/send-to-joey-snippet.html").rstrip("\n")

# 2. quick-look prompts -------------------------------------------------------
src = R("shared/quick-look.src.md")
APPS = {
    "chatgpt/quick-look-prompt.md": {
        "SEARCH_LINE": "Use your memory of our past conversations, all of them, as far back as you can see.",
        "SETTING_LINE": "Settings > Personalization > Memory, turn on memory and \"Reference chat history\" (names vary a little by plan), and don't use a Temporary chat.",
        "APP": "ChatGPT",
        "CHECK_HINT": "",
        "MENU": (
            "   - Custom instructions (Settings > Personalization > Custom instructions). Give both boxes filled in with my real details: what I do, where, how I talk to customers, how you should answer. This is almost always number one.\n"
            "   - A Project for the thing I do over and over (quotes, follow-ups, a kind of email), with instructions written out and what to pin in it.\n"
            "   - Memory: the exact line I say once so you remember a fact for good (\"Remember that I ...\")."),
        "FILE_LINE": "Write the whole report as one HTML file I can download, with simple clean styling: light gray background, white cards, lots of space, one section per screen, the set-once blocks in copy boxes.",
        "SOURCE": "chatgpt-quick-look",
        "OPEN_LINE": "Open the file in your browser, read it, and click Send to Joey at the top.",
    },
    "claude-app/quick-look-prompt.md": {
        "SEARCH_LINE": "Search our past chats, all of them, as far back as you can see, and use what you find.",
        "SETTING_LINE": "Settings > Capabilities (on some accounts it's under Settings > Memory), turn on \"Search and reference chats\", and don't use an incognito chat. Searching past chats needs a paid plan (Pro or higher); on the free plan the six questions are the way in.",
        "APP": "Claude",
        "CHECK_HINT": " If you have a tool to search past chats, run it a few times with different words (quotes, customers, jobs, invoices, texts) before you decide.",
        "MENU": (
            "   - Personal preferences (Settings > Profile, or Settings > General on some accounts, then the personal preferences box). Give the block filled in with my real details: what I do, where, how I talk to customers, how you should answer. It applies to every chat and works on every plan. This is almost always number one.\n"
            "   - A Project with instructions for the thing I do over and over (quotes, follow-ups, a kind of email). New project > name it > Project instructions > paste. Give the instructions written out and what to add to its knowledge.\n"
            "   - Memory: the exact line I say once so you remember a fact for good (\"Remember that I ...\"), if my plan has memory.\n"
            "   - A Style (the style menu under the chat box > Create and edit styles) for how texts and emails should sound, if that's a pattern."),
        "FILE_LINE": "Write the whole report as one HTML file I can download and open in my browser, with simple clean styling: light gray background, white cards, lots of space, one section per screen, the set-once blocks in copy boxes. Make it a real downloadable file, not an artifact preview, because the Send button has to reach the internet. If you can only make an artifact, say so and tell me to use its download button and open the file in my browser.",
        "SOURCE": "claude-quick-look",
        "OPEN_LINE": "Download the file, open it in your browser, read it, and click Send to Joey at the top.",
    },
}
for out, vals in APPS.items():
    s = src
    for k, v in dict(vals, SNIPPET=snippet).items():
        s = s.replace("@@" + k + "@@", v)
    left = re.findall(r"@@[A-Z_]+@@", s)
    if left: sys.exit(f"{out}: unfilled {left}")
    W(out, s)

# 3. audit pack ---------------------------------------------------------------
def replace_block(text, heading, fence, body):
    """Replace the first ```fence block that comes after `heading`. Fails loudly if it can't find it."""
    i = text.find(heading)
    if i < 0: sys.exit(f"audit-pack.md: can't find {heading!r}")
    start = text.find("```" + fence + "\n", i)
    if start < 0: sys.exit(f"audit-pack.md: no ```{fence} block after {heading!r}")
    start += len("```" + fence + "\n")
    end = text.find("\n```\n", start)
    if end < 0: sys.exit(f"audit-pack.md: unclosed block after {heading!r}")
    return text[:start] + body.rstrip("\n") + text[end:]

pack = R("chatgpt/audit-pack.md")
pack = replace_block(pack, "**5d.", "html", snippet)
pack = replace_block(pack, "## Reader script", "python", R("skills/ai-standing/scripts/read_history.py"))
pack = replace_block(pack, "## Report template", "html", R("skills/ai-standing/templates/report.html"))
W("chatgpt/audit-pack.md", pack)

# 4. example opportunities page ----------------------------------------------
subprocess.run([sys.executable, str(root / "skills/ai-interview/scripts/build_opportunities.py"),
                "--profile", str(root / "examples/example-profile.json"),
                "--write", str(root / "sample-opportunities.html")], check=True)
print("Done.")
