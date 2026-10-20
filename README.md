# Where You Stand with AI

An AI check-up for owners of trades and service businesses: HVAC, plumbing, roofing, landscaping, electrical, and the like. Built by Joey Farbstein (LocalPro Solutions).

How it works:

1. **The quick look (about 5 minutes).** You paste one prompt into ChatGPT or Claude. It looks at how you already use AI, puts you on a four-rung ladder, and writes you a short report with three things to set up once and a roadmap. New to AI? That's fine. It asks you six quick questions instead.
2. **The interview (about 20 minutes).** Paste the block at the bottom of your report into any AI. It asks plain questions about how your business runs: calls, scheduling, quotes, follow-up, reviews, invoices.
3. **Your opportunities page.** A ranked list of what AI could take off your plate, with hours back a week and what each one takes.
4. **A call with Joey.** Both pages have a **Send to Joey** button and a **Book a call with Joey** button.

The four rungs: **1** You type, it answers. **2** It knows your business. **3** It's hooked up to your tools. **4** It runs jobs without you.

## Start here

| You use | Do this |
|---|---|
| ChatGPT | Open the [ChatGPT quick-look prompt](https://raw.githubusercontent.com/ThetaOneMarketing/joeyfarbstein-ai/main/chatgpt/quick-look-prompt.md), copy all of it, paste it into a new ChatGPT chat on a computer, send. More in [chatgpt/README.md](chatgpt/README.md). |
| Claude (claude.ai or the Claude app) | Open the [Claude quick-look prompt](https://raw.githubusercontent.com/ThetaOneMarketing/joeyfarbstein-ai/main/claude-app/quick-look-prompt.md), copy all of it, paste it into a new chat, send. More in [claude-app/README.md](claude-app/README.md). |
| ChatGPT, and you want exact numbers | Export your chats, then attach the export plus the [full audit pack](https://raw.githubusercontent.com/ThetaOneMarketing/joeyfarbstein-ai/main/chatgpt/audit-pack.md). Steps in [chatgpt/README.md](chatgpt/README.md#full-audit-exact-counts). |
| Claude Code | Install the plugin (below) and run `/ai-standing`. |

When the report is done, open it in your browser, click **Send to Joey** at the top, and copy the block at the bottom into any AI to start the interview. The interview instructions it points to live at
https://raw.githubusercontent.com/ThetaOneMarketing/joeyfarbstein-ai/main/skills/ai-interview/SKILL.md

Want to see what you get first? Examples with made-up businesses: [sample-report.html](sample-report.html) and [sample-opportunities.html](sample-opportunities.html) (download and open in a browser).

## Claude Code plugin

    /plugin marketplace add ThetaOneMarketing/joeyfarbstein-ai
    /plugin install joeyfarbstein-ai@joeyfarbstein-ai

Then:

    /ai-standing ~/.claude/projects              Claude Code users, no export needed
    /ai-standing ~/Downloads/data-export.zip     claude.ai or ChatGPT export

When the report opens, say "go" to start the interview. Or later: `/ai-interview`.

## The booking link (one setting)

Every "Book a call with Joey" button reads one value: `BOOKING_URL` in [config.json](config.json).

    {
      "BOOKING_URL": "REPLACE_WITH_BOOKING_URL"
    }

1. Put Joey's real scheduling link there (it must start with `https://`).
2. Run `python3 chatgpt/build_pack.py`. That copies the link into both quick-look prompts, the audit pack, both page templates, the interview instructions, and the sample pages.
3. Commit and push.

Until it's set, the buttons say "Email Joey to book a call" and open an email to joe@localprosolutions.com. There's no made-up link anywhere.

## What's inside

    config.json                                    the booking link (see above)
    shared/quick-look.src.md                       the one source both quick-look prompts are built from
    chatgpt/quick-look-prompt.md                   ChatGPT quick look (built, don't edit by hand)
    claude-app/quick-look-prompt.md                Claude quick look (built, don't edit by hand)
    chatgpt/audit-pack.md                          full audit for a ChatGPT export (embedded parts are rebuilt)
    chatgpt/send-to-joey-snippet.html              the Send to Joey / Book a call bar the quick-look reports carry
    chatgpt/build_pack.py                          rebuilds everything above from its sources
    skills/ai-standing/SKILL.md                    the audit, for Claude Code
    skills/ai-standing/scripts/read_history.py     reads Claude Code, claude.ai, and ChatGPT history into one shape
    skills/ai-standing/scripts/handoff.py          uploads the audit and writes the interview block into the report
    skills/ai-standing/templates/report.html       the report page
    skills/ai-interview/SKILL.md                   the 20-minute interview
    skills/ai-interview/scripts/build_opportunities.py   turns the interview's profile.json into the opportunities page
    skills/ai-interview/scripts/upload_results.py  adds the interview files to the same audit bundle
    skills/ai-interview/templates/opportunities.html     the opportunities page
    examples/example-profile.json                  the made-up data behind sample-opportunities.html
    server/                                        the upload endpoint Joey runs (see server/README.md)
    TESTING.md                                     how to test it by hand
    FOR-COLLABORATORS.md                           why it's built this way, and what's left

After editing a skill, the snippet, the shared prompt source, or config.json, run `python3 chatgpt/build_pack.py` so the built files match.

Where the reports go: the Send to Joey button (and `handoff.py` in Claude Code) posts to Joey's upload endpoint, which saves them in the `audits` storage bucket under an unlisted 12-character id. See [server/README.md](server/README.md) and [TESTING.md](TESTING.md#check-that-the-upload-reached-joey).
