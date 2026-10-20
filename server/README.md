# Audit upload endpoint

Where the audit bundles go. One Supabase edge function plus one storage bucket.

## One-time setup

1. In your Supabase project, create a storage bucket named `audits`. Mark it **public** (anyone with the link can read; nobody can write without this function).
2. Deploy the function:

       supabase functions deploy audit-upload --no-verify-jwt

3. Your endpoint is `https://<project-ref>.supabase.co/functions/v1/audit-upload`.
   It's written in four places. If it ever changes, change all four:
   - `skills/ai-standing/scripts/handoff.py` (`DEFAULT_UPLOAD_URL`, or set `AUDIT_UPLOAD_URL` in the environment)
   - `skills/ai-interview/scripts/upload_results.py` (same env variable)
   - `chatgpt/send-to-joey-snippet.html` (then run `python3 chatgpt/build_pack.py`)
   - `skills/ai-interview/templates/opportunities.html`

The function reads the project URL and service key from the environment Supabase gives every edge function (`SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`). No key is stored in this repo, and none should be.

Joey's live endpoint is on the `open-brain` project, bucket `audits`. Nothing in this repo deploys it; deploying is a manual step.

## What a bundle looks like

    https://<ref>.supabase.co/storage/v1/object/public/audits/x7k2pq9d3m/
      findings.json   what the audit found
      report.html     the report they read
      session.md      the chat that produced it
      index.json      list of files + upload time
      (after the interview) interview.md, profile.json, opportunities.html, interview-session.md

Ids are 12 random characters (about 60 bits), so links can't be guessed. Every audit anyone runs lands in this bucket, so you see every lead and its full context before the call.

## Checking that an upload arrived

See [TESTING.md](../TESTING.md#check-that-the-upload-reached-joey).

## Later

Point a custom domain (e.g. `audit.joeyfarbstein.com`) at the bucket if you want cleaner links. Not needed to work.
