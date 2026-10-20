# For collaborators (and their AI agents)

Joey Farbstein built this with Claude on October 13, 2026. If you're an AI agent reading this because someone asked you to help on the project, this is the context you need. Plain language on purpose; Joey's collaborators are not all developers.

## What this is

An AI audit for contractors: roofers, HVAC, landscapers, plumbers. It reads a person's own AI chat history, tells them where they stand with AI, hands them three things to set up once, and then interviews them about the parts of their business that never showed up in those chats. The end product is a ranked list of AI agents that would fit their business, with a confidence meter and an hours-back meter on each, and a button to book a call with Joey.

It's the first step of Joey's "AI operating system for contractors" offer. The audit is cheap or free. The call sells the setup.

## Why it's built the way it is

**It copies the shape of Claude Code's own `/insights` report.** That report reads your sessions and writes eight sections: a summary, what you work on, how you work, wins, friction, features to try, new habits, and what's on the horizon. Every suggestion in it is something you set up once and the AI installs. Joey wanted that for contractors. The structure, the evidence rule (every claim cites a count or a quote), and the "set once" rule all come from there.

**Tone is for a contractor.** Short sentences. No "leverage," "workflow," "optimize," "integration," "automation." Hours a week, not percentages. No hype, no exclamation points, no emoji. The report is a diagnosis with their own words as proof, not a sales pitch. It sells one thing, once, at the end: the interview.

**The ladder is the spine.** Four rungs: you type and it answers; it knows your business; it's hooked up to your tools; it runs jobs without you. Almost every contractor is on rung 1. The whole report points at the ladder so they can see where they are and the quickest step up.

**Quick wins must be set-once.** Joey's first run produced "paste this prompt every morning." He rejected it: that's a chore. The rule now is that every quick win is a one-time install (CLAUDE.md block, a skill, a hook, a scheduled task, custom instructions, a project, a phone text shortcut) and after that it works on its own. The report tells them the exact clicks or says "paste this into Claude Code and it sets it up."

**Export is too much friction.** The first ChatGPT path asked people to export their chats and wait for an email. Joey killed it: ChatGPT already remembers past chats, so the quick look just asks it. Rough numbers, no waiting. The export path stays as the deeper option.

**No button on the report.** The last thing on the page is a visible block of text with a copy icon. Paste it into any AI, anywhere, any day, and the interview starts with full context. A button can't launch a chat; a prompt can.

**The handoff is a bundle with a link.** When the audit finishes it writes three files (what it found, the report itself, and the whole chat that produced it), uploads them to Joey's Supabase, and gets back a private link with a random id. The copy-paste prompt carries that link, the local folder path, and the GitHub link to the interview instructions. A fresh session in a different app can start cold. Every audit anyone runs lands in Joey's bucket, so he sees each lead before the call.

**Ship both skills in one package.** Joey asked whether the audit should fetch the interview from a link when needed. Answer: no, put both in one plugin so there's nothing to download mid-session. The GitHub link in the prompt is the fallback for a session that doesn't have the plugin.

**Buy the agents, build the glue.** Earlier the same day Joey decided the eventual agents for clients should be off-the-shelf tools (a voice answering service, an invoice chaser) rather than custom builds, with one shared memory (Open Brain) that everything logs to. That decision isn't in this repo yet; it shapes what the opportunities page recommends.

## What exists

| Path | What it is | State |
|---|---|---|
| `skills/ai-standing/SKILL.md` | The audit: what to read, what to find, how to write the eight sections, tone rules, the set-once menu, the handoff | Working. Joey ran it on himself. |
| `skills/ai-standing/scripts/read_history.py` | Turns a Claude Code folder, a claude.ai export, or a ChatGPT export into one simple shape plus counts | Tested on all three. Needs to filter out scheduled and headless runs on Claude Code folders (see FIRST-RUN-NOTES.md). |
| `skills/ai-standing/scripts/handoff.py` | Bundles findings + report + chat, uploads to Supabase, writes the copy-paste prompt into the report | Working. Live upload confirmed. |
| `skills/ai-standing/templates/report.html` | The report page. Tailwind, light gray, one idea per screen, collapsible cards, scroll-spy nav | Done. |
| `skills/ai-interview/SKILL.md` | The interview | Stub: loads the bundle, plays it back, asks three questions. The real seven-topic version is next. |
| `skills/ai-interview/templates/opportunities.html` | The final page: ranked agents with confidence and hours-back meters, effort tag, book-a-call | Template done; sample at `sample-opportunities.html`. |
| `skills/ai-interview/scripts/upload_results.py` | Adds the interview's files to the same bundle | Written, not yet run live. |
| `server/supabase/functions/audit-upload/index.ts` | The upload endpoint | Deployed on Joey's `open-brain` project, bucket `audits`, public read, random 12-char ids. |
| `chatgpt/quick-look-prompt.md` | The one-paste audit for ChatGPT. Uses ChatGPT's own memory of past chats, no export. The report embeds a Send-to-Joey bar that uploads from the browser | Built, not yet tested on a real account. This is the default path for non-Claude users. |
| `chatgpt/audit-pack.md` | The full audit as one file a ChatGPT user attaches alongside their export | Built, not yet tested. The deeper option for exact counts. |
| `.claude-plugin/` | Plugin and marketplace manifests | Install: `/plugin marketplace add ThetaOneMarketing/joeyfarbstein-ai` then `/plugin install joeyfarbstein-ai@joeyfarbstein-ai` |
| `sample-report.html` | The report template filled with a made-up roofer | For seeing the look. All example data. |

## How to run it

Claude Code: `/ai-standing ~/.claude/projects`, then say `go` when it offers the interview.

ChatGPT: paste `chatgpt/quick-look-prompt.md` into a new chat. No export. See `chatgpt/README.md` for the full-export version.

claude.ai: same as ChatGPT in principle; the pack hasn't been adapted for it yet.

## What's next, in order

1. The real interview. Seven topics: basics, how work comes in, day to day, money, tools, customers, the pain. Don't leave a topic until there's a real example, a tool name, and a rough time cost. Short follow-ups, one question at a time, playback every couple of topics. Ends by writing `interview.md`, `profile.json`, and `opportunities.html`, then uploading. Text first; voice later.
2. Test on a real contractor's ChatGPT export. Everything so far was tested on developers' histories, which read "rung 4" and sound techy. The product is for rung 1 people.
3. The reader should skip scheduled and headless sessions in Claude Code folders on its own.
4. A claude.ai edition of the pack.

## Rules Joey set

- Go slow. Say the plan before building anything big.
- Dummy proof. If a step could confuse a non-technical person, it's wrong.
- Contractor tone, always, in everything the person sees.
- Run the humanizer pass (the `humanizer` skill) on any prose a person will read.
- No button on the report. A copy-paste prompt.
- Set once, works forever. Never a routine they have to remember.
