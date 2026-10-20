# ChatGPT edition

Two ways in. The quick look is the default; the full audit is for exact numbers.

## Quick look (default, about 5 minutes)

No export. ChatGPT uses what it remembers from past chats. If it can't see any (new account, or memory off), it asks six quick questions instead and writes the report from the answers.

1. Open the prompt: https://raw.githubusercontent.com/ThetaOneMarketing/joeyfarbstein-ai/main/chatgpt/quick-look-prompt.md
2. Copy all of it. Paste it into a new ChatGPT chat on a computer (not a Temporary chat). Send.
3. If it asks six questions, answer them. Short answers are fine.
4. It hands back the report as an HTML file and shows the At a glance part in the chat.
5. Download the file, open it in your browser, click **Send to Joey** at the top. That sends the report to Joey from your browser (ChatGPT's own sandbox can't reach the internet, so the page does it). **Book a call with Joey** is right next to it.
6. Copy the block at the bottom of the report into a new chat to start the 20-minute interview.

Numbers are rough ("about a third of our chats") because memory is a summary, not a log. The report says so.

To let ChatGPT see past chats: Settings > Personalization > Memory, turn on memory and "Reference chat history." Names vary a little by plan.

## Full audit (exact counts)

1. Export: ChatGPT > Settings > Data controls > Export data > Confirm. An email link arrives in minutes to an hour. Download the zip.
2. Download the pack: https://raw.githubusercontent.com/ThetaOneMarketing/joeyfarbstein-ai/main/chatgpt/audit-pack.md (right-click, Save as).
3. New chat, attach both files, paste: `Read audit-pack.md and follow it on the attached export. Don't explain, just do it.`
4. The report comes back as a download with the same Send to Joey and Book a call bar.

## For whoever maintains this

Don't edit `quick-look-prompt.md` by hand. It's built from `../shared/quick-look.src.md`. The embedded script, template, and snippet in `audit-pack.md` are built from the skill. After changing any of those, or `../config.json`, run from the repo root:

    python3 chatgpt/build_pack.py

## Files

- `quick-look-prompt.md`  the one-paste audit (built)
- `audit-pack.md`         the full audit, attached alongside an export
- `send-to-joey-snippet.html`  the Send to Joey / Book a call bar both reports carry
- `build_pack.py`         rebuilds the prompts, the pack, and the sample pages
