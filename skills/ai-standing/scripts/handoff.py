#!/usr/bin/env python3
"""
handoff.py — bundle the audit, upload it, and write the copy-paste prompt into the report.

Usage:
  python3 handoff.py --out ai-standing-out [--upload-url URL] [--no-upload]

Expects these in --out (the audit skill writes them):
  findings.json   what the audit found (rung, buckets, key pattern, quick wins, not_seen ...)
  report.html     the finished report
  session.md      the chat that produced the report, as the AI wrote it down

Does, in this order:
  1. Uploads findings.json and session.md to the audit endpoint. Gets back a link like
     https://<host>/audits/x7k2pq9d3m/  (unguessable id, read-only)
  2. Writes start-interview.txt: the prompt the person pastes into any AI to start the interview.
  3. Fills that prompt into report.html where {{INTERVIEW_PROMPT}} is, and rewrites the file.
  4. Uploads the filled report.html into the same bundle (same id).
     (The first run uploaded the report before step 3, so Joey's copy had an empty prompt box.)

If upload fails or --no-upload, the prompt still gets written with the local folder path only,
so the handoff works on the same computer.

Env:
  AUDIT_UPLOAD_URL   overrides the default endpoint
"""
import argparse, json, os, sys, urllib.request, uuid, mimetypes, html
from pathlib import Path

DEFAULT_UPLOAD_URL = os.environ.get(
    "AUDIT_UPLOAD_URL",
    "https://svivkeuiydxloyyrcrna.supabase.co/functions/v1/audit-upload",
)
REPO = "https://github.com/ThetaOneMarketing/joeyfarbstein-ai"
INTERVIEW_RAW = "https://raw.githubusercontent.com/ThetaOneMarketing/joeyfarbstein-ai/main/skills/ai-interview/SKILL.md"
FILES = ["findings.json", "report.html", "session.md"]


def multipart(fields: dict, files: list):
    """Build a multipart/form-data body by hand (no requests dependency)."""
    boundary = "----audit" + uuid.uuid4().hex
    body = b""
    for k, v in fields.items():
        body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n").encode()
    for name, path in files:
        ctype = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"; filename=\"{path.name}\"\r\n"
                 f"Content-Type: {ctype}\r\n\r\n").encode() + path.read_bytes() + b"\r\n"
    body += f"--{boundary}--\r\n".encode()
    return body, f"multipart/form-data; boundary={boundary}"


def upload(out: Path, url: str, names, bundle_id=None):
    present = [(f, out / f) for f in names if (out / f).exists()]
    fields = {"id": bundle_id} if bundle_id else {}
    body, ctype = multipart(fields, present)
    req = urllib.request.Request(url, data=body, method="POST",
                                 headers={"Content-Type": ctype, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read().decode())
    if "url" not in data:
        raise RuntimeError(f"upload endpoint returned no url: {data}")
    return data["url"].rstrip("/") + "/", data.get("id")


def build_prompt(bundle_url: str | None, local_dir: Path, findings: dict):
    who = findings.get("name") or "a contractor"
    rung = findings.get("rung", "?")
    lines = ["Start my AI interview."]
    if bundle_url:
        lines.append(
            f"My audit is here: {bundle_url}\n"
            f"It has three files: findings.json (what the audit found), report.html (the report I read), "
            f"and session.md (the chat that produced it). Download and read all three before you say anything."
        )
    lines.append(
        f"If you're on the same computer the audit ran on, the same three files are in {local_dir.resolve()}/ and you can read them there instead."
    )
    lines.append(
        f"The interview instructions are here: {INTERVIEW_RAW}\n"
        f"Fetch them and follow them exactly. (Full project: {REPO})"
    )
    lines.append(
        f"I'm {who}, on rung {rung} of 4. Open with a one-line playback of what the audit found, then ask your first question. Don't explain the process."
    )
    return "\n\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="ai-standing-out")
    ap.add_argument("--upload-url", default=DEFAULT_UPLOAD_URL)
    ap.add_argument("--no-upload", action="store_true")
    a = ap.parse_args()
    out = Path(a.out)
    missing = [f for f in FILES if not (out / f).exists()]
    if "findings.json" in missing or "report.html" in missing:
        sys.exit(f"Missing in {out}: {missing}. The audit must write findings.json and report.html first.")
    if "session.md" in missing:
        print("Warning: session.md not found. The interview won't see the chat history. Continuing.")

    findings = json.loads((out / "findings.json").read_text())
    bundle_url, bundle_id = None, None
    if not a.no_upload and "REPLACE-WITH" not in a.upload_url:
        try:
            # report.html goes up last, after the interview prompt is written into it
            bundle_url, bundle_id = upload(out, a.upload_url, ["findings.json", "session.md"])
            print(f"Uploaded findings. Bundle link: {bundle_url}")
        except Exception as e:
            print(f"Upload failed ({e}). Falling back to local-only handoff.")
    elif "REPLACE-WITH" in a.upload_url:
        print("No upload endpoint configured (AUDIT_UPLOAD_URL). Local-only handoff.")

    prompt = build_prompt(bundle_url, out, findings)
    (out / "start-interview.txt").write_text(prompt)
    findings["bundle_url"] = bundle_url
    (out / "findings.json").write_text(json.dumps(findings, indent=2))

    rp = out / "report.html"
    h = rp.read_text()
    if "{{INTERVIEW_PROMPT}}" in h:
        h = h.replace("{{INTERVIEW_PROMPT}}", html.escape(prompt))
        rp.write_text(h)
        print("Prompt written into report.html.")
    else:
        print("report.html had no {{INTERVIEW_PROMPT}} slot; prompt is in start-interview.txt.")

    if bundle_url and bundle_id:
        try:
            upload(out, a.upload_url, ["report.html"], bundle_id)
            print(f"Uploaded report. Joey's copy: {bundle_url}report.html")
        except Exception as e:
            print(f"Report upload failed ({e}). findings.json and session.md are up; the report is only local.")
    print("\n--- paste this into any AI to start the interview ---\n")
    print(prompt)


if __name__ == "__main__":
    main()
