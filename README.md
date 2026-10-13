# joeyfarbstein-ai

Two skills for contractors and local service businesses, packaged as one Claude Code plugin.

1. **ai-standing** — "Where You Stand with AI." Reads your AI chat history (Claude Code folder, claude.ai export, or ChatGPT export) and writes a plain report: where you are on the four-rung ladder, three things to do tonight, and one glimpse of what's next.
2. **ai-interview** — The 20-minute interview that follows. Picks up where the audit left off and asks about the parts of your business that never showed up in your chats.

## Install (Claude Code)

    /plugin marketplace add ThetaOneMarketing/joeyfarbstein-ai
    /plugin install joeyfarbstein-ai@joeyfarbstein-ai

## Run

    /ai-standing ~/.claude/projects              Claude Code users, no export needed
    /ai-standing ~/Downloads/data-export.zip     claude.ai or ChatGPT export

When the report opens, say "go" to start the interview. Or later: `/ai-interview`.

## What's inside

    skills/ai-standing/SKILL.md               how the report gets written
    skills/ai-standing/scripts/read_history.py reads all three chat formats into one shape
    skills/ai-standing/scripts/handoff.py      bundles findings + report + chat, uploads, writes the paste-in prompt
    server/                                   the Supabase upload endpoint (one-time setup, see server/README.md)
    skills/ai-standing/templates/report.html   the page that gets filled in
    skills/ai-interview/SKILL.md              the interview (stub for now)

The audit uploads findings.json, report.html, and session.md to your Supabase bucket and puts a copy-paste prompt at the bottom of the report. Paste that into any AI, anywhere, and the interview picks up with full context. Same computer: it also reads ai-standing-out/ directly.
