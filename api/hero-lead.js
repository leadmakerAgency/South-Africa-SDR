// Vercel Serverless Function: POST /api/hero-lead
//
// Relays the homepage hero email capture to the n8n webhook.
// The webhook URL is kept server-side in the N8N_HERO_WEBHOOK_URL environment
// variable (Vercel → Project → Settings → Environment Variables) so it never
// appears in the page source or in this public repository.
//
// Safeguards: POST only, same-site Origin check, payload size limit, strict
// email validation, honeypot (_gotcha) handling, and an upstream timeout.

const MAX_EMAIL_LENGTH = 254;
const MAX_URL_LENGTH = 2000;
const UPSTREAM_TIMEOUT_MS = 8000;
const EMAIL_RE = /^[^\s@<>()[\]\\,;:"]+@[^\s@<>()[\]\\,;:"]+\.[A-Za-z]{2,}$/;

const ALLOWED_HOSTS = new Set(["southafricasdr.com", "www.southafricasdr.com", "south-africa-sdr.vercel.app"]);
// Vercel preview / branch deployments of this project
const PREVIEW_HOST_RE = /^south-africa-[a-z0-9-]+-leadmakeragencys-projects\.vercel\.app$/;

function allowedOrigin(origin) {
  if (!origin) return false;
  try {
    const u = new URL(origin);
    if (u.protocol === "http:" && (u.hostname === "localhost" || u.hostname === "127.0.0.1")) return true;
    return u.protocol === "https:" && (ALLOWED_HOSTS.has(u.hostname) || PREVIEW_HOST_RE.test(u.hostname));
  } catch {
    return false;
  }
}

function readBody(req) {
  try {
    const body = req.body; // parsed by Vercel for application/json; throws on invalid JSON
    if (body && typeof body === "object") return body;
    if (typeof body === "string" && body.length <= 4096) return JSON.parse(body);
  } catch {
    /* fall through */
  }
  return null;
}

// Only pass along a page URL that belongs to the same site the request came from.
function cleanPageUrl(value, origin) {
  if (typeof value !== "string" || value.length > MAX_URL_LENGTH) return null;
  try {
    const page = new URL(value);
    return page.origin === new URL(origin).origin ? page.href : null;
  } catch {
    return null;
  }
}

module.exports = async function handler(req, res) {
  res.setHeader("Cache-Control", "no-store");

  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ ok: false, error: "method_not_allowed" });
  }

  const origin = req.headers.origin;
  if (!allowedOrigin(origin)) {
    return res.status(403).json({ ok: false, error: "forbidden" });
  }

  const body = readBody(req);
  if (!body) {
    return res.status(400).json({ ok: false, error: "invalid_body" });
  }

  // Honeypot filled in → almost certainly a bot. Pretend success, forward nothing.
  if (typeof body._gotcha === "string" && body._gotcha.trim() !== "") {
    return res.status(204).end();
  }

  const email = typeof body.email === "string" ? body.email.trim() : "";
  if (!email || email.length > MAX_EMAIL_LENGTH || !EMAIL_RE.test(email)) {
    return res.status(400).json({ ok: false, error: "invalid_email" });
  }

  const webhookUrl = process.env.N8N_HERO_WEBHOOK_URL;
  if (!webhookUrl) {
    console.error("[hero-lead] N8N_HERO_WEBHOOK_URL is not configured");
    return res.status(500).json({ ok: false, error: "not_configured" });
  }

  const payload = {
    email,
    source: "hero",
    page_url: cleanPageUrl(body.page_url, origin),
    country: req.headers["x-vercel-ip-country"] || null,
    submitted_at: new Date().toISOString(),
  };

  try {
    const upstream = await fetch(webhookUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(UPSTREAM_TIMEOUT_MS),
    });
    if (!upstream.ok) {
      // Never log the email address — status only.
      console.error(`[hero-lead] n8n webhook responded ${upstream.status}`);
      return res.status(502).json({ ok: false, error: "upstream_error" });
    }
    return res.status(204).end();
  } catch (err) {
    console.error(`[hero-lead] n8n webhook request failed: ${err && err.name}`);
    return res.status(502).json({ ok: false, error: "upstream_unreachable" });
  }
};
