// Contact form handler: validates the submission and emails it via Resend.
const TO = "connect@kickstarttechsolutions.com";
const DEFAULT_FROM = "Kickstart Tech Solutions Website <website@updates.kickstarttechsolutions.com>";

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });

const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

export async function onRequestPost({ request, env }) {
  let data;
  try {
    const type = request.headers.get("Content-Type") || "";
    data = type.includes("application/json") ? await request.json() : Object.fromEntries(await request.formData());
  } catch {
    return json({ ok: false, error: "Invalid request" }, 400);
  }

  // Honeypot: bots fill hidden fields, people do not.
  if (data._honey) return json({ ok: true });

  const f = {};
  for (const k of ["name", "company", "email", "phone", "interest", "message"]) f[k] = String(data[k] || "").trim().slice(0, 5000);
  if (!f.name || !f.company || !f.email) return json({ ok: false, error: "Missing required fields" }, 400);
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(f.email)) return json({ ok: false, error: "Invalid email" }, 400);
  // Turnstile: once a secret is configured, every submission must carry a valid token.
  if (env.TURNSTILE_SECRET_KEY) {
    const token = String(data["cf-turnstile-response"] || "");
    if (!token) return json({ ok: false, error: "Verification required" }, 403);
    const form = new FormData();
    form.append("secret", env.TURNSTILE_SECRET_KEY);
    form.append("response", token);
    const ip = request.headers.get("CF-Connecting-IP");
    if (ip) form.append("remoteip", ip);
    const check = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", { method: "POST", body: form });
    const outcome = await check.json().catch(() => ({}));
    if (!outcome.success) return json({ ok: false, error: "Verification failed" }, 403);
  }

  if (!env.RESEND_API_KEY) return json({ ok: false, error: "Email is not configured" }, 500);

  const rows = [
    ["Name", f.name], ["Business", f.company], ["Email", f.email], ["Phone", f.phone || "Not given"],
    ["Interested in", f.interest || "Not given"], ["Message", f.message || "No message"],
  ];
  const html = `<h2 style="font-family:sans-serif">New assessment request</h2><table cellpadding="6" style="font-family:sans-serif;border-collapse:collapse">${rows
    .map(([k, v]) => `<tr><td style="font-weight:bold;vertical-align:top">${k}</td><td>${esc(v).replace(/\n/g, "<br>")}</td></tr>`)
    .join("")}</table>`;
  const text = rows.map(([k, v]) => `${k}: ${v}`).join("\n");

  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify({
      from: env.RESEND_FROM || DEFAULT_FROM,
      to: [env.CONTACT_TO || TO],
      reply_to: f.email,
      subject: `New assessment request: ${f.company}`,
      html,
      text,
    }),
  });
  if (!res.ok) {
    console.log("Resend error", res.status, await res.text());
    return json({ ok: false, error: "Could not send" }, 502);
  }
  return json({ ok: true });
}
