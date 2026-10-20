# Testing by hand

Three runs, then a check that the upload arrived. Do them on a computer, in Chrome, Safari, or Edge. Plan about an hour for all of it.

Every test upload lands in Joey's real `audits` bucket. Put **TEST** in the business name when you answer questions so it's easy to spot, and delete test folders afterward (see the end).

The copy-paste links point at the `main` branch. Until this work is merged into `main`, copy the prompt from the branch on GitHub instead (open the file, click **Raw**, copy all).

## Before you start

- [ ] `config.json` has the booking link you want to test, or the placeholder (then the button should say "Email Joey to book a call").
- [ ] You ran `python3 chatgpt/build_pack.py` after the last change, and it printed `Done.`
- [ ] Open `sample-report.html` and `sample-opportunities.html` in a browser. Both show a yellow **EXAMPLE** banner. The Book a call buttons go to the booking link (or open an email to Joey).

## Test 1: brand-new ChatGPT account (no history)

1. Make a fresh ChatGPT account (free is fine), or use one with memory turned off.
2. New chat, not a Temporary chat. Paste all of https://raw.githubusercontent.com/ThetaOneMarketing/joeyfarbstein-ai/main/chatgpt/quick-look-prompt.md and send.
3. **Expect:** one line saying it can't see past chats, then six numbered questions in one message. It must not stop, refuse, or make up a history.
4. Answer as a made-up HVAC shop: "TEST Heating, Boise, 3 techs plus me. Nothing yet. Mostly calls from Google. Goes to voicemail, I call back at night. Invoices. Calling people back."
5. **Expect:** a downloadable HTML file, the At a glance part in the chat, and the line about opening the file.
6. Download and open the file. Go through "What to check in the report" below.
7. Click **Send to Joey**. **Expect:** the bar says "Sent. Joey has it." and the interview block at the bottom now ends with "My audit is saved here: …" and a link.
8. Copy the interview block into a new ChatGPT chat. **Expect:** a one-line playback, then one question. Answer about ten questions, then try "I'm out of time." It should wrap up and still produce the opportunities page. See "What to check on the opportunities page."

## Test 2: brand-new Claude account (no history)

1. Make a fresh claude.ai account (free plan: past-chat search isn't available, which is the point of this test).
2. New chat, not incognito. Paste all of https://raw.githubusercontent.com/ThetaOneMarketing/joeyfarbstein-ai/main/claude-app/quick-look-prompt.md and send.
3. **Expect:** the same as Test 1: one line, six questions, no refusal. After the report, one line saying past-chat search needs a paid plan and where the setting is.
4. Answer as a made-up plumber: "TEST Plumbing, Austin, just me and my brother. Used it to write a Facebook post once. Calls and referrals. Voicemail. Quotes. Quotes."
5. **Expect:** a real downloadable HTML file. If it only makes an artifact preview, it should say so and tell you to download it. Open the downloaded file in the browser (the Send button doesn't work inside the preview).
6. Same checks as Test 1, steps 6 to 8.

## Test 3: someone with a lot of history

Use a ChatGPT or Claude account that has months of real chats, ideally a contractor's. Joey's own account works but reads as rung 4 and techy.

1. Paste the matching quick-look prompt.
2. **Expect:** no questions. It goes straight to the report.
3. The report quotes or paraphrases real chats, uses "about" for counts, and puts the person on a believable rung.
4. Claude Code version, if you have it: `/ai-standing ~/.claude/projects`. The reader prints how many sessions it skipped as "not the person typing". On Joey's folder that should be most of them (about 2,500 of about 2,750). Then check `ai-standing-out/start-interview.txt` exists and the report's interview block is filled in.

## What to check in the report

- [ ] All eight sections are there: At a glance, The ladder, What you use it for, How you work with it, Where it paid off, Where it let you down, Three things to set up once, Where this leaves you.
- [ ] For a no-history run, the line "Built from your answers to six questions, not from a long chat history." is under the title, and thin sections are one honest line, not padding.
- [ ] Nothing made up: no invented quotes, chat counts, or customers. Every claim matches the history or the answers.
- [ ] The three set-once fixes are each done once in settings (custom instructions, personal preferences, a project, memory, a style, a text shortcut). None says "paste this at the start of every chat."
- [ ] The roadmap has three steps. For the HVAC and plumber test answers (calls going to voicemail), step 1 is about not losing missed calls, said plainly, with no product names and no prices.
- [ ] Plain words. None of: leverage, workflow, optimize, integration, automation, efficiency, streamline, unlock, solution, robust, seamless. No percentages, no exclamation points, no emoji.
- [ ] Nothing personal, medical, or about a named customer is quoted.
- [ ] A **Book a call with Joey** button at the end of section 8 and in the top bar. It goes to the booking link, or says "Email Joey to book a call" if the link isn't set. It never goes to a dead or made-up page.
- [ ] The interview block is in a box with a working copy button, and includes the GitHub link to the interview instructions.
- [ ] The page looks right on a phone-width window too.

## What to check on the opportunities page

- [ ] No yellow EXAMPLE banner (that's only on the sample).
- [ ] 3 to 8 cards, biggest hours first. Each has a one-line plain description, hours back a week, an effort tag (Tonight / An afternoon / Hook up your tools), and a how-sure level.
- [ ] Hours match what you said in the interview. Guesses say "(our guess)".
- [ ] Every card shows "Price: Not set yet. Joey goes over it on the call." No dollar figures anywhere.
- [ ] For the test answers above, a missed-call card is at or near the top.
- [ ] **Send to Joey** works (see below) and **Book a call with Joey** goes to the booking link or opens an email.

## Check that the upload reached Joey

After clicking **Send to Joey** on a report or opportunities page:

1. The bar should say "Sent. Joey has it." If it says "That didn't go through", note the message in brackets.
2. The interview block at the bottom of the report now has a link like
   `https://svivkeuiydxloyyrcrna.supabase.co/storage/v1/object/public/audits/<12 characters>/report.html`.
   Open it. You should see the report.
3. Open the same address with `index.json` in place of `report.html`. It lists the files in the bundle (`findings.json`, `report.html`, and after the interview `profile.json`, `opportunities.html`, maybe `interview.md`) and an `updated_at` time.
4. In the Supabase dashboard (Joey's account, `open-brain` project): **Storage > audits**. There's a folder with that 12-character name and the same files. Newest folders are at the bottom unless you sort by date.
5. Claude Code path: `handoff.py` prints "Uploaded findings. Bundle link: …" and then "Uploaded report. Joey's copy: …". Open that report link and check the interview block is filled in (the first run uploaded it empty).

Clean up: in **Storage > audits**, delete the TEST folders. Deleting is permanent, so only delete the ones you made.

If the Send button fails every time: open the browser's developer tools (right-click > Inspect > Network), click Send again, and look at the `audit-upload` request. A 400 says what's missing; a 500 means the function or bucket has a problem, which is Joey's to check in Supabase (Edge Functions > audit-upload > Logs).
