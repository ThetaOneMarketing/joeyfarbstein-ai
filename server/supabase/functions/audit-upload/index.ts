// audit-upload — receives the audit bundle (findings.json, report.html, session.md),
// stores it under an unguessable id in the public "audits" bucket, returns the link.
//
// Deploy:  supabase functions deploy audit-upload --no-verify-jwt
// Bucket:  create a PUBLIC bucket named "audits" (read is public, write is only via this function).
//
// Returns: { "id": "x7k2pq9d3m", "url": "https://<ref>.supabase.co/storage/v1/object/public/audits/x7k2pq9d3m/" }
// Files land at <url>findings.json, <url>report.html, <url>session.md, <url>index.json

import { createClient } from "https://esm.sh/@supabase/supabase-js@2.45.4";

const ALLOWED = new Set(["findings.json", "report.html", "session.md"]);
const MAX_BYTES = 15 * 1024 * 1024;
const ALPHABET = "abcdefghijkmnpqrstuvwxyz23456789";

function newId(len = 12) {
  const bytes = crypto.getRandomValues(new Uint8Array(len));
  return Array.from(bytes, (b) => ALPHABET[b % ALPHABET.length]).join("");
}

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  if (req.method !== "POST") return new Response("POST only", { status: 405, headers: cors });

  let form: FormData;
  try {
    form = await req.formData();
  } catch {
    return Response.json({ error: "expected multipart/form-data" }, { status: 400, headers: cors });
  }

  const files: { name: string; blob: File }[] = [];
  for (const [, v] of form.entries()) {
    if (v instanceof File && ALLOWED.has(v.name)) {
      if (v.size > MAX_BYTES) return Response.json({ error: `${v.name} too large` }, { status: 413, headers: cors });
      files.push({ name: v.name, blob: v });
    }
  }
  if (!files.some((f) => f.name === "findings.json")) {
    return Response.json({ error: "findings.json is required" }, { status: 400, headers: cors });
  }

  const url = Deno.env.get("SUPABASE_URL")!;
  const key = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
  const sb = createClient(url, key);
  const id = newId();

  for (const f of files) {
    const type = f.name.endsWith(".json") ? "application/json" : f.name.endsWith(".html") ? "text/html" : "text/markdown";
    const { error } = await sb.storage.from("audits").upload(`${id}/${f.name}`, f.blob, { contentType: type, upsert: false });
    if (error) return Response.json({ error: error.message }, { status: 500, headers: cors });
  }
  const index = { id, files: files.map((f) => f.name), uploaded_at: new Date().toISOString() };
  await sb.storage.from("audits").upload(`${id}/index.json`, new Blob([JSON.stringify(index, null, 2)]), { contentType: "application/json" });

  const publicUrl = `${url}/storage/v1/object/public/audits/${id}/`;
  return Response.json({ id, url: publicUrl, files: index.files }, { headers: cors });
});
