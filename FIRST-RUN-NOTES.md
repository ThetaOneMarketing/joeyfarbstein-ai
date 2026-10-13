# Notes from the first real run (Joey, Oct 13, 2026)

Step 4 of HANDOFF.md, run on Joey's own Claude Code folder. The chain works end to end: install, read, report, upload, prompt. Audit id `hqcb8ur32pm9`. These are the bugs and gaps it shook out.

## Bugs

1. **The reader counts robot runs as the person's chats.** `read_history.py` read 2,753 chats. 2,541 of them were scheduled jobs, headless runs, subagents, and workflow sessions, not Joey typing. Only 212 were real. The audit had to filter by hand: keep only project folders that start with `-Users-`, and drop any chat whose first message has a headless marker (`<scheduled-task`, `running headless`, `Print exactly`, `RESULT: OK`, `/insights`, and so on). The reader should do this itself for Claude Code folders. A roofer on claude.ai or ChatGPT will not hit this.
2. **The reader also counts machine messages as the person's words.** Task notifications, `<bash-input>` echoes, image placeholders, skill bodies, and "Request interrupted" markers all show up as `who: me`. About 1,000 of 3,433 messages. Median message length and one-message counts are wrong until these are dropped.
3. **Timezone.** The handoff said Los Angeles. The data said Europe for July to late August, then Los Angeles. The skill asks once, which is right, but the reader could flag a shift: if the hour-of-day pattern changes mid-span, say so.
4. **`handoff.py` uploads `report.html` before it writes the interview prompt into it.** The copy at the public link has an empty `{{INTERVIEW_PROMPT}}` slot. Either upload after filling, or upload twice.
5. **Footer says "Nothing here was shared with anyone."** The bundle is uploaded to a public, unguessable link by design. The line should say that instead.
6. **Manifests failed `claude plugin validate`.** `$schema` is not allowed in either manifest, and the marketplace `description` must live under `metadata`. Fixed and pushed in commit 5f95642.

## Gaps

- The "one rung up" box has nothing to say for a rung 4 person. The report used it for "a rung 4 you can trust." Fine for Joey. Decide what it says for a real rung 4 client, if one ever shows up.
- Copy buttons and the collapsible rungs need JavaScript. They work in a normal browser. They do not work in a static preview.
- The reader produced a 22 MB `chats.jsonl` for Joey. Fine, but a slow laptop will feel it.

## What worked

- Reader handled 2.4 GB and 2,830 session files in about a minute.
- Upload endpoint, public bucket, and raw GitHub link all returned 200.
- Template filled with zero banned words, zero em dashes, zero percent signs, zero exclamation points on the first pass.
