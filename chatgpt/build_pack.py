#!/usr/bin/env python3
"""Rebuild chatgpt/audit-pack.md from the ai-standing skill. Run from the repo root."""
# (same assembly as used on 2026-10-13; see README. Kept short on purpose: edit the skill, not the pack.)
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
skill = (root/"skills/ai-standing/SKILL.md").read_text()
reader = (root/"skills/ai-standing/scripts/read_history.py").read_text()
tpl = (root/"skills/ai-standing/templates/report.html").read_text()
pack = (root/"chatgpt/audit-pack.md").read_text()
# refresh only the two embedded blocks; the prose edits live in audit-pack.md itself
pack = re.sub(r"```python\n.*?\n```", "```python\n"+reader+"\n```", pack, count=1, flags=re.S)
pack = re.sub(r"```html\n.*?\n```", "```html\n"+tpl+"\n```", pack, count=1, flags=re.S)
(root/"chatgpt/audit-pack.md").write_text(pack)
print("audit-pack.md refreshed")
