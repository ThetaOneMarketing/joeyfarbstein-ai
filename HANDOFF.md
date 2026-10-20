# Handoff for Claude Code

> **History, not current.** This is the October 13 handoff that got the repo created and the first run done. The repo exists now and steps 1 to 4 are done. For the current state, read [FOR-COLLABORATORS.md](FOR-COLLABORATORS.md); for testing, [TESTING.md](TESTING.md). The interview is no longer a stub (see `skills/ai-interview/SKILL.md`).

Read this first. You're picking up a project Joey built with Claude on claude.ai on Oct 13, 2026. Everything you need is in this folder. The job right now is to get it onto GitHub and run a real test. Plain language, short steps. Joey is not a developer; explain anything you do in one line each.

## What this is

A two-skill Claude Code plugin for contractors (roofers, HVAC, landscapers, plumbers). It's the first step of Joey's "AI operating system for contractors" funnel.

1. **ai-standing** ("Where You Stand with AI"). Reads a person's AI chat history (their Claude Code folder, or a claude.ai or ChatGPT export) and writes a plain-spoken report: where they sit on a four-rung ladder, what they use AI for, three things to do tonight, and one glimpse of what's next. Tone rules are strict: short sentences, no AI hype, banned-word list, a humanizer pass.
2. **ai-interview**. The 20-minute interview that follows. Right now it's a stub (three questions) that proves the handoff works. The full seven-topic version is the next build.

The handoff between the two is the clever part. When the audit finishes it writes three files (findings.json, report.html, session.md), uploads them to Joey's Supabase, gets back a private link, and puts a copy-paste prompt at the bottom of the report. Paste that prompt into any AI, anywhere, any day, and the interview picks up with full context. Same computer: it also reads the local folder.

## Current state

- All code is written and tested as far as possible from the cloud.
- The reader script works on all three chat formats (tested).
- The report template renders (tested, sample at the bottom of this file).
- The Supabase upload endpoint is deployed and live on the `open-brain` project (`svivkeuiydxloyyrcrna`): function `audit-upload`, public bucket `audits`. A real upload from Joey's Mac succeeded (id `sd4h3dw8q8mg`).
- The handoff script `skills/ai-standing/scripts/handoff.py` already points at that endpoint.
- The GitHub repo does NOT exist yet. That's blocking: the prompt at the bottom of every report points at it.

## Do this, in order

### 1. Create the repo and push

The repo must be public and named exactly `ThetaOneMarketing/joeyfarbstein-ai` (every link in the project already points there).

```
cd <this folder>
git init
git add -A
git commit -m "Where You Stand with AI: audit + interview plugin"
gh repo create ThetaOneMarketing/joeyfarbstein-ai --public --source=. --push
```

If `gh` isn't installed: `brew install gh` then `gh auth login`, then the commands above. If Joey would rather click: github.com/new, owner ThetaOneMarketing, name joeyfarbstein-ai, Public, no README; then `git remote add origin https://github.com/ThetaOneMarketing/joeyfarbstein-ai.git && git push -u origin main`.

### 2. Check the one link that matters

Open this in a browser. It must show the interview skill, not a 404:

https://raw.githubusercontent.com/ThetaOneMarketing/joeyfarbstein-ai/main/skills/ai-interview/SKILL.md

That's the link inside every copy-paste prompt. If it 404s, nothing downstream works.

### 3. Install the plugin on this Mac

```
/plugin marketplace add ThetaOneMarketing/joeyfarbstein-ai
/plugin install joeyfarbstein-ai@joeyfarbstein-ai
```

Then `/ai-standing` and `/ai-interview` should show up as commands.

### 4. Run the audit on Joey himself

```
/ai-standing ~/.claude/projects
```

It'll ask his timezone once (America/Los_Angeles). Then it reads everything, writes the report, uploads the bundle, and asks "want to do the interview? say go." Expected output folder: `ai-standing-out/` with `findings.json`, `report.html`, `session.md`, `start-interview.txt`.

Known caveat: Joey's own history is a weird test case. He's on rung 4 and talks like a developer, so the report will read differently than it will for a roofer. The point of this run is to shake out bugs, not to judge the writing. The real test is a client's export.

### 5. Say "go" and watch the stub interview

It should open with a one-line playback of the audit, then ask about the first thing in `not_seen`. Three questions, then it stops and writes `interview-notes.md`.

### 6. Test the cold path

Open a brand-new Claude Code session in a different folder. Paste the contents of `ai-standing-out/start-interview.txt`. It should fetch the bundle from the Supabase link, fetch the interview skill from GitHub, and open with the same playback. If it works cold, the whole chain works.

## What's next after that (not for this session unless Joey says so)

- Write the full interview (`skills/ai-interview/SKILL.md`). Seven topics: basics, how work comes in, day-to-day, money, tools, customers, the pain. Relentless follow-up: don't move on until each topic has a real example, a tool name, and a rough time cost. Voice-first later; text first.
- Companion guide for claude.ai and ChatGPT users: how to export their chats, and the audit as a paste-in prompt instead of a skill.
- Maybe a custom domain for the audit links (`audit.joeyfarbstein.com`) so they look cleaner. Not required.

## Files

```
.claude-plugin/plugin.json, marketplace.json    plugin + marketplace manifests
README.md                                        install + run, for the public
skills/ai-standing/SKILL.md                      how the report gets written (the brain)
skills/ai-standing/scripts/read_history.py       3 chat formats -> one shape + counts
skills/ai-standing/scripts/handoff.py            bundle, upload, write the paste-in prompt
skills/ai-standing/templates/report.html         the page (Tailwind, light gray, collapsible)
skills/ai-interview/SKILL.md                     the interview (stub)
server/supabase/functions/audit-upload/index.ts  the upload endpoint (already deployed)
server/README.md                                 how the endpoint was set up
sample-report.html                               the template filled with made-up roofer data, to see the look
```

## Rules Joey set, keep them

- Tone is always for a contractor. Short, plain, respectful. No "leverage," "workflow," "optimize," "integration," "automation." Numbers they feel (hours a week, jobs a month), never percentages.
- The report is not a sales pitch. It diagnoses, proves it with their own words, gives real value, and points to the interview once at the end.
- No button on the report. A visible copy-paste prompt.
- Dummy proof. If a step could confuse a non-technical person, it's wrong.
- Go slow. Tell Joey the plan before building anything big.
