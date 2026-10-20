#!/usr/bin/env python3
"""
upload_results.py — add the interview's results to the audit bundle in Joey's Supabase.

Usage:
  python3 upload_results.py --out ai-standing-out

Expects in --out:
  findings.json        from the audit (has "bundle_url" if the audit uploaded)
  interview.md         their answers, in their words, by topic
  profile.json         structured facts: trade, crew, tools, time sinks, numbers, agents
  opportunities.html   the finished "What AI could run for you" page
  interview-session.md (optional) the interview chat, word for word

If findings.json has a bundle_url, the files are added to that same bundle (same id), so one link holds
the audit, the interview, and the results. If not, a new bundle is created.

Prints the link to opportunities.html when done.
"""
import argparse, json, os, re, sys, urllib.request, uuid, mimetypes
from pathlib import Path

UPLOAD_URL = os.environ.get("AUDIT_UPLOAD_URL", "https://svivkeuiydxloyyrcrna.supabase.co/functions/v1/audit-upload")
FILES = ["interview.md", "profile.json", "opportunities.html", "interview-session.md"]


def multipart(fields, files):
    boundary = "----audit" + uuid.uuid4().hex
    body = b""
    for k, v in fields.items():
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
    for name, path in files:
        ctype = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"; filename=\"{path.name}\"\r\n"
                 f"Content-Type: {ctype}\r\n\r\n").encode() + path.read_bytes() + b"\r\n"
    body += f"--{boundary}--\r\n".encode()
    return body, f"multipart/form-data; boundary={boundary}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="ai-standing-out")
    a = ap.parse_args()
    out = Path(a.out)
    present = [(f, out / f) for f in FILES if (out / f).exists()]
    if not any(f == "opportunities.html" for f, _ in present):
        sys.exit(f"opportunities.html not found in {out}. Build the page first.")

    fields = {}
    findings_path = out / "findings.json"
    if findings_path.exists():
        bundle_url = json.loads(findings_path.read_text()).get("bundle_url") or ""
        m = re.search(r"/audits/([a-z0-9]{12})/?$", bundle_url)
        if m:
            fields["id"] = m.group(1)
        else:
            present.insert(0, ("findings.json", findings_path))  # new bundle needs it

    body, ctype = multipart(fields, present)
    req = urllib.request.Request(UPLOAD_URL, data=body, method="POST",
                                 headers={"Content-Type": ctype, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            data = json.loads(r.read().decode())
    except Exception as e:
        print(f"Upload failed: {e}. Results are still in {out}/.")
        return
    url = data.get("url", "").rstrip("/") + "/"
    (out / "results-link.txt").write_text(url + "opportunities.html\n")
    if findings_path.exists():
        f = json.loads(findings_path.read_text()); f["bundle_url"] = url; f["results_url"] = url + "opportunities.html"
        findings_path.write_text(json.dumps(f, indent=2))
    print(f"Uploaded. Results page: {url}opportunities.html")
    print(f"Whole bundle: {url}")


if __name__ == "__main__":
    main()
