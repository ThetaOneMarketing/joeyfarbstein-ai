# Audit upload endpoint

Where the audit bundles go. One Supabase edge function plus one storage bucket.

## One-time setup

1. In your Supabase project, create a storage bucket named `audits`. Mark it **public** (anyone with the link can read; nobody can write without this function).
2. Deploy the function:

       supabase functions deploy audit-upload --no-verify-jwt

3. Your endpoint is `https://<project-ref>.supabase.co/functions/v1/audit-upload`.
   Put it in `skills/ai-standing/scripts/handoff.py` as `DEFAULT_UPLOAD_URL`, or set `AUDIT_UPLOAD_URL` in the environment.

## What a bundle looks like

    https://<ref>.supabase.co/storage/v1/object/public/audits/x7k2pq9d3m/
      findings.json   what the audit found
      report.html     the report they read
      session.md      the chat that produced it
      index.json      list of files + upload time

Ids are 12 random characters (about 60 bits), so links can't be guessed. Every audit anyone runs lands in this bucket, so you see every lead and its full context before the call.

## Later

Point a custom domain (e.g. `audit.joeyfarbstein.com`) at the bucket if you want cleaner links. Not needed to work.
