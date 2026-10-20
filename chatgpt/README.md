# ChatGPT edition

Two ways in. The quick look is the default; the full audit is for exact numbers.

## Quick look (default, about 5 minutes)

No export. ChatGPT uses its own memory of the person's past chats.

1. Copy `quick-look-prompt.md`, all of it.
2. Paste into a new ChatGPT chat on a computer. Send.
3. It hands back the report as an HTML download and shows the At-a-glance in chat.
4. Open the report, click **Send to Joey** at the top. That posts the report to Joey's Supabase bucket from the browser (ChatGPT's sandbox can't reach the internet, so the page does it instead).

Numbers are rough ("about a third of our chats") because memory is a summary, not a log. The report says so.

If memory is off: Settings > Personalization > Memory > Reference chat history.

## Full audit (exact counts)

1. Export: ChatGPT > Settings > Data controls > Export data > Confirm. Email link arrives, minutes to an hour. Download the zip.
2. Download `audit-pack.md`.
3. New chat, attach both files, paste: `Read audit-pack.md and follow it on the attached export. Don't explain, just do it.`
4. Report comes back as a download, with the same Send to Joey bar.

`audit-pack.md` is built from the Claude Code skill. After changing the skill, run `python3 chatgpt/build_pack.py` to refresh the embedded script and template.

## Files

- `quick-look-prompt.md`  the one-paste audit
- `audit-pack.md`         the full audit, attached alongside an export
- `send-to-joey-snippet.html`  the upload bar both reports embed
- `build_pack.py`         refreshes audit-pack.md from the skill
