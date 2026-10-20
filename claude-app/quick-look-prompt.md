Give me my "Where You Stand with AI" report. Search our past chats, all of them, as far back as you can see, and use what you find. Don't ask me questions first. Just do it.

If you can't search past chats (the setting is off, or there's nothing there), stop and tell me exactly that, in one line, and tell me to turn on "Search and reference chats" in Settings. Don't make anything up.

WHO I AM
I run a small business. Figure out what kind from our chats. If you can't tell, say so. I'm busy and I'm not a tech person.

WHAT YOU'RE DOING
Look at everything you remember about how I use you, and write me a plain report. Not a sales pitch. A mirror. The goal is that I read it and think "huh, it noticed something about me I hadn't."

RULES
- Talk like someone who's been on a job site. Short sentences. Plain words.
- Never use these words: leverage, workflow, optimize, integration, automation, efficiency, streamline, unlock, revolutionary, AI-powered, solution, utilize, robust, seamless, delve.
- Numbers I feel: hours a week, jobs a month, dollars. Never percentages.
- No hype. No exclamation points. No emoji. No dashes as connectors.
- Every claim points at something real from our chats. Quote me when you can. If you're working from memory and not exact counts, say "about" and "from what I remember." Never invent a number.
- Don't quote anything personal, medical, financial, or about a named customer. Paraphrase or skip.
- Respect me. I run a business. Don't talk down, don't cheerlead, don't over-explain.

THE REPORT, in this order, each section short

1. AT A GLANCE. Four short paragraphs: what's working (where you're already pulling your weight for me), what's holding me back (the biggest pattern costing me), tonight (name the three set-once things in one line each), the bigger picture (one sentence of what it looks like when AI is hooked up and running for me, and that a 20-minute interview finds the rest).

2. THE LADDER. Four rungs. Tell me which one I'm on and why, in my terms, with evidence.
   Rung 1: You type, it answers. Every chat starts from zero.
   Rung 2: It knows your business. Your prices, your customers, how you talk.
   Rung 3: It's hooked up to your tools. Your calendar, your invoices, your texts.
   Rung 4: It runs jobs without you. Follow-ups go out. Quotes get drafted. You check in.
   Then two short paragraphs: WHERE YOU ARE NOW (what it's costing me) and ONE RUNG UP (what changes for me specifically). Then one or two sentences on why this ladder is the whole point.

3. WHAT I USE YOU FOR. Up to five buckets, each with a rough share ("about a third of our chats") and one sentence with an example. Use my words for the bucket names when you can. End with one or two sentences on what this means for me: hours, money, or the ladder.

4. HOW I WORK WITH YOU. Three or four short paragraphs. Do I fire off one question and leave, or work with you? What do I trust you with, and what do I never bring to you? Do I re-explain who I am every time? Where did I give up after a bad answer? End with one bold sentence: my key pattern. Then one or two sentences on what this means for me.

5. WHERE YOU'VE ALREADY PAID OFF. Three wins. Title, then two or three sentences with proof from our chats. Then one or two sentences on what this means for me.

6. WHERE YOU LET ME DOWN. Three patterns. Each: title, the pattern in one or two sentences, two real examples (paraphrased), a one-sentence fix. Then one or two sentences on what this means for me.

7. THREE THINGS TO SET UP ONCE. This is the most important section. The rule: each one is set up ONCE and works every time after. Never "paste this at the top of every chat." Never a routine I have to remember. If I'd have to do it again tomorrow, it's a chore, not a win. Each must come from something you saw, be free, take about ten minutes, need no new accounts, and end with a block I copy once plus the exact clicks.
   Pick from this menu:
   - A Project with instructions. New project > name it after my business > Project instructions > paste. Give the block filled in with my real details: what I do, where, how I talk to customers, how you should answer. From then on every chat in that project knows me. This is almost always number one.
   - A second Project for the thing I do over and over (quotes, follow-ups, a kind of email), with instructions written out and what to add to its knowledge.
   - Memory: the exact line I say once so you remember a fact for good ("Remember that I ...").
   - A Style (Settings > Styles) for how texts and emails should sound, if that's a pattern.
   - iPhone text replacement (Settings > General > Keyboard > Text Replacement) for a message I keep rewriting: give the full text and a short code.
   Format each: title, Why (one line of evidence), what changes after (one or two sentences starting "From now on"), the exact clicks, then the block.

8. WHERE THIS LEAVES ME. One scene, two or three sentences, of what it looks like when AI is running on its own for my business, built from my real stuff. Then: my rung restated in one line. Tonight: the one thing to do first and which rung it gets me to. Then: this report could only see what I've brought to you; the stuff that eats my week that I've never thought to use AI for doesn't show up here, and 20 minutes of questions finds the rest. Name two or three business areas that never came up in our chats.

   End with this block, filled in, inside a code box so I can copy it:

   Start my AI interview.
   My quick-look audit found: rung {N}. I use AI mostly for {top two or three buckets}. Key pattern: {the bold sentence}. Three set-once fixes: {titles}. Never showed up in my chats: {the areas}.
   The interview instructions are here: https://raw.githubusercontent.com/ThetaOneMarketing/joeyfarbstein-ai/main/skills/ai-interview/SKILL.md
   Read them and follow them exactly. Open with a one-line playback of what the audit found, then ask your first question. Don't explain the process.

HOW TO HAND IT OVER
Write the whole report as one HTML file I can download and open in my browser, with simple clean styling: light gray background, white cards, lots of space, one section per screen, the set-once blocks in copy boxes. Make it a real downloadable file, not an artifact preview, because the Send button has to reach the internet. If you can only make an artifact, say so and tell me to use its download button and open the file in my browser.

Put this block right after <body>, exactly as written. Replace {{FINDINGS_JSON}} with a JSON object: {"name","business","rung","buckets":[{"name","share"}],"key_pattern","wins":[],"friction":[],"quick_wins":[],"not_seen":[],"source":"claude-quick-look"}. It's a button that sends the report to Joey when I click it.

<!-- SEND TO JOEY: put this right after <body>. It posts this page and the findings to Joey's audit bucket when clicked. -->
<div id="stj" style="position:sticky;top:0;z-index:50;background:#1b2430;color:#fff;padding:12px 20px;display:flex;align-items:center;justify-content:space-between;gap:12px;font-family:Inter,system-ui,sans-serif">
  <span style="font-size:14px;opacity:.85">Done reading? Send this report to Joey so he has it before you talk.</span>
  <button id="stj-btn" type="button" style="background:#f5b400;color:#3d2e00;font-weight:700;border:0;border-radius:10px;padding:10px 16px;cursor:pointer;font-size:14px">Send to Joey</button>
</div>
<script id="stj-findings" type="application/json">{{FINDINGS_JSON}}</script>
<script>
(function(){
  var btn=document.getElementById('stj-btn'), bar=document.getElementById('stj');
  var URL='https://svivkeuiydxloyyrcrna.supabase.co/functions/v1/audit-upload';
  btn.addEventListener('click', async function(){
    btn.disabled=true; btn.textContent='Sending...';
    try{
      var fd=new FormData();
      var findings=document.getElementById('stj-findings').textContent;
      fd.append('findings.json', new Blob([findings],{type:'application/json'}), 'findings.json');
      fd.append('report.html', new Blob(['<!doctype html>\n'+document.documentElement.outerHTML],{type:'text/html'}), 'report.html');
      var r=await fetch(URL,{method:'POST',body:fd});
      var j=await r.json();
      if(!r.ok||!j.url) throw new Error(j.error||('HTTP '+r.status));
      bar.querySelector('span').textContent='Sent. Joey has it.';
      btn.textContent='Sent'; btn.style.background='#0f766e'; btn.style.color='#fff';
      try{localStorage.setItem('stj-sent',j.url);}catch(e){}
    }catch(e){
      btn.disabled=false; btn.textContent='Try again';
      bar.querySelector('span').textContent='Could not send ('+e.message+'). Check your internet and try again, or email the file to joe@localprosolutions.com.';
    }
  });
  try{ if(localStorage.getItem('stj-sent')){ bar.querySelector('span').textContent='Already sent to Joey.'; btn.textContent='Sent'; btn.disabled=true; btn.style.background='#0f766e'; btn.style.color='#fff'; } }catch(e){}
})();
</script>


Also show me section 1 (At a glance) right here in the chat. Then one line: "Download the file, open it in your browser, read it, and click Send to Joey at the top. The block at the bottom starts the interview whenever you're ready."

If you can't make a file, give me the whole report here in the chat instead, formatted cleanly, and tell me to copy it into an email to joe@localprosolutions.com. Don't skip sections.
