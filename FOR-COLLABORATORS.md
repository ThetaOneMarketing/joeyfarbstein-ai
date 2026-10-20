# For collaborators (and their AI agents)

Joey Farbstein built this with Claude on October 13, 2026. If you're an AI agent reading this because someone asked you to help on the project, this is the context you need. Plain language on purpose; Joey's collaborators are not all developers.

## What this is

An AI audit for contractors: roofers, HVAC, landscapers, plumbers. It reads a person's own AI chat history (or, if they're new to AI, asks them six quick questions), tells them where they stand with AI, hands them three things to set up once and a three-step roadmap, and then interviews them about the parts of their business that never showed up in those chats. The end product is a ranked list of things AI could take off their plate, each with a plain description, hours back a week, an effort level, a how-sure meter, and a price placeholder Joey fills in on the call, plus a button to book a call with Joey.

It's the first step of Joey's "AI operating system for contractors" offer. The audit is cheap or free. The call sells the setup.

## Why it's built the way it is

**It copies the shape of Claude Code's own `/insights` report.** That report reads your sessions and writes eight sections: a summary, what you work on, how you work, wins, friction, features to try, new habits, and what's on the horizon. Every suggestion in it is something you set up once and the AI installs. Joey wanted that for contractors. The structure, the evidence rule (every claim cites a count or a quote), and the "set once" rule all come from there.

**Tone is for a contractor.** Short sentences. No "leverage," "workflow," "optimize," "integration," "automation." Hours a week, not percentages. No hype, no exclamation points, no emoji. The report is a diagnosis with their own words as proof, not a sales pitch. It sells one thing, once, at the end: the interview.

**The ladder is the spine.** Four rungs: you type and it answers; it knows your business; it's hooked up to your tools; it runs jobs without you. Almost every contractor is on rung 1. The whole report points at the ladder so they can see where they are and the quickest step up.

**Quick wins must be set-once.** Joey's first run produced "paste this prompt every morning." He rejected it: that's a chore. The rule now is that every quick win is a one-time install (CLAUDE.md block, a skill, a hook, a scheduled task, custom instructions, a project, a phone text shortcut) and after that it works on its own. The report tells them the exact clicks or says "paste this into Claude Code and it sets it up."

**Export is too much friction.** The first ChatGPT path asked people to export their chats and wait for an email. Joey killed it: ChatGPT already remembers past chats, so the quick look just asks it. Rough numbers, no waiting. The export path stays as the deeper option.

**No button to start the interview.** The interview starts from a visible block of text with a copy icon at the bottom of the report. Paste it into any AI, anywhere, any day, and the interview starts with full context. A button can't launch a chat; a prompt can.

**One booking button, one setting.** The report and the opportunities page each end with "Book a call with Joey." Every one of those buttons reads `BOOKING_URL` from `config.json`; `python3 chatgpt/build_pack.py` copies it everywhere. Until Joey sets it, the buttons say "Email Joey to book a call" and open an email to him. No made-up links.

**New to AI is the normal case.** Most contractors have little or no chat history, and Claude's past-chat search needs a paid plan. So the quick look never stops on an empty history: it asks six short questions (business, what they've used AI for, how customers reach them, what happens to missed calls, the office job that eats their week, what they'd hand off) and writes the report from the answers, saying so at the top.

**The roadmap leads with missed calls when it fits.** For trades businesses, a missed call is usually a lost job. When the chats or answers point that way, roadmap step 1 is "Stop losing the calls you can't answer," in plain words, no product names, no prices. This is where Joey's Missed-Call Rescue offer fits, but the report never pitches it; if calls aren't the problem, it leads with the real gap.

**The handoff is a bundle with a link.** When the audit finishes it writes three files (what it found, the report itself, and the whole chat that produced it), uploads them to Joey's Supabase, and gets back a private link with a random id. The copy-paste prompt carries that link, the local folder path, and the GitHub link to the interview instructions. A fresh session in a different app can start cold. Every audit anyone runs lands in Joey's bucket, so he sees each lead before the call.

**Ship both skills in one package.** Joey asked whether the audit should fetch the interview from a link when needed. Answer: no, put both in one plugin so there's nothing to download mid-session. The GitHub link in the prompt is the fallback for a session that doesn't have the plugin.

**Buy the agents, build the glue.** Earlier the same day Joey decided the eventual agents for clients should be off-the-shelf tools (a voice answering service, an invoice chaser) rather than custom builds, with one shared memory (Open Brain) that everything logs to. That decision isn't in this repo yet; it shapes what the opportunities page recommends.

## What exists

| Path | What it is | State |
|---|---|---|
| `config.json` | The one setting: `BOOKING_URL` for every "Book a call with Joey" button | Placeholder. Joey needs to put his real link in, then run the build. |
| `shared/quick-look.src.md` | The single source for both quick-look prompts | Edit this, not the built prompts. |
| `chatgpt/quick-look-prompt.md` | The one-paste audit for ChatGPT. Uses ChatGPT's memory of past chats; asks six questions if it can't see any. The report carries a Send to Joey and Book a call bar | Built from the source. Not yet tested on a real account (see TESTING.md). This is the default path for non-Claude users. |
| `claude-app/quick-look-prompt.md` | Same, for claude.ai | Built from the source. Not yet tested on a real account. |
| `chatgpt/audit-pack.md` | The full audit as one file a ChatGPT user attaches alongside their export | Built, not yet tested. The deeper option for exact counts. |
| `chatgpt/send-to-joey-snippet.html` | The bar at the top of quick-look reports: Send to Joey (uploads from the browser) and Book a call | Done. After sending, it adds the saved-report link to the interview block. |
| `chatgpt/build_pack.py` | Rebuilds the prompts, the pack's embedded parts, the booking link everywhere, and the sample opportunities page | Run after any change to a source. |
| `skills/ai-standing/SKILL.md` | The audit: what to read, what to find, how to write the eight sections and the roadmap, tone rules, the set-once menu, the handoff | Working. Joey ran it on himself. |
| `skills/ai-standing/scripts/read_history.py` | Turns a Claude Code folder, a claude.ai export, or a ChatGPT export into one simple shape plus counts | Fixed after the first run: skips scheduled, headless, subagent, and temp-folder sessions and machine messages in Claude Code folders; reads only the kept branch of ChatGPT chats and drops hidden custom-instructions messages; flags a possible timezone move. Tested on small made-up files of all three kinds, not yet re-run on Joey's real folder. |
| `skills/ai-standing/scripts/handoff.py` | Uploads the audit, writes the copy-paste interview block into the report, then uploads the filled report | Fixed after the first run: the report now goes up after the block is written. Tested against a local stand-in for the endpoint, not the live one. |
| `skills/ai-standing/templates/report.html` | The report page. Tailwind, light gray, one idea per screen, collapsible cards, roadmap, Book a call button | Done. |
| `skills/ai-interview/SKILL.md` | The interview: 16 plain questions (plus 2 optional), one at a time, about 20 minutes. Then it works out ranked opportunities with hours back and effort and writes the page | Written. Not yet run with a real contractor. |
| `skills/ai-interview/scripts/build_opportunities.py` | Checks the interview's `profile.json` (no prices, sane hours, effort and confidence set), ranks it, and writes `opportunities.html` | Done and tested on the example. |
| `skills/ai-interview/templates/opportunities.html` | The final page, drawn from the JSON the interview writes: ranked cards, hours back, effort, how sure, price placeholder, Send to Joey, Book a call | Done. |
| `skills/ai-interview/scripts/upload_results.py` | Adds the interview's files to the same bundle | Written, not yet run live. |
| `examples/example-profile.json` | Made-up shop used to build `sample-opportunities.html` | Clearly labeled EXAMPLE. |
| `server/supabase/functions/audit-upload/index.ts` | The upload endpoint | Deployed on Joey's `open-brain` project, bucket `audits`, public read, random 12-character ids. Reads its keys from the environment. |
| `.claude-plugin/` | Plugin and marketplace manifests | Pass `claude plugin validate`. Install: `/plugin marketplace add ThetaOneMarketing/joeyfarbstein-ai` then `/plugin install joeyfarbstein-ai@joeyfarbstein-ai` |
| `sample-report.html`, `sample-opportunities.html` | The two pages filled with made-up businesses | For seeing the look. Both have an EXAMPLE banner. |
| `TESTING.md` | Manual test script: fresh ChatGPT, fresh Claude, rich history, and checking the upload | New. |

## How to run it

Claude Code: `/ai-standing ~/.claude/projects`, then say `go` when it offers the interview.

ChatGPT: paste `chatgpt/quick-look-prompt.md` into a new chat. No export. See `chatgpt/README.md` for the full-export version.

claude.ai: paste `claude-app/quick-look-prompt.md` into a new chat. See `claude-app/README.md`.

Interview, anywhere: paste the block from the bottom of the report into a new chat. It points at `skills/ai-interview/SKILL.md` on GitHub.

The copy-paste links in the READMEs and in the prompts point at the `main` branch on GitHub. They only work once these files are merged into `main`.

## What's next, in order

1. Joey sets `BOOKING_URL` in `config.json` and runs `python3 chatgpt/build_pack.py`.
2. Joey decides prices. The opportunities page only shows a placeholder ("Price: Not set yet. Joey goes over it on the call."). Nothing in the repo invents a price.
3. Run TESTING.md end to end: a fresh ChatGPT account, a fresh Claude account, and a rich history. Then one real contractor. Everything so far was tested on developers' histories, which read "rung 4" and sound techy. The product is for rung 1 people.
4. Re-run the reader on Joey's real Claude Code folder and check that the chat count drops to about the 212 real ones.
5. Voice version of the interview, later.

## Rules Joey set

- Go slow. Say the plan before building anything big.
- Dummy proof. If a step could confuse a non-technical person, it's wrong.
- Contractor tone, always, in everything the person sees.
- Run the humanizer pass (the `humanizer` skill) on any prose a person will read.
- No button to start the interview. A copy-paste prompt. (The one button is Book a call with Joey, at the end.)
- Set once, works forever. Never a routine they have to remember.
