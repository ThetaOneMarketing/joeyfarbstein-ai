# Claude app (claude.ai) edition

Same as the ChatGPT quick look. Claude searches your past chats itself, so there's no export. If it can't (free plan, setting off, or a new account), it asks six quick questions instead and writes the report from the answers.

1. Open the prompt: https://raw.githubusercontent.com/ThetaOneMarketing/joeyfarbstein-ai/main/claude-app/quick-look-prompt.md
2. Copy all of it. Paste it into a new chat at claude.ai on a computer (not an incognito chat). Send.
3. If it asks six questions, answer them. Short answers are fine.
4. Download the report it makes, open it in your browser, click **Send to Joey** at the top. **Book a call with Joey** is right next to it.
5. Copy the block at the bottom of the report into a new chat to start the 20-minute interview.

To let Claude search past chats: Settings > Capabilities (on some accounts, Settings > Memory), turn on "Search and reference chats." It needs a paid plan (Pro or higher).

The prompt is built from `../shared/quick-look.src.md` by `python3 chatgpt/build_pack.py`. Don't edit it by hand.

Claude Code users don't need this; they install the plugin (see the main README).
