# Kickstart Tech Solutions website

Static multi-page site for Kickstart Tech Solutions: Hardware, Networking, Managed IT and Cloud, and Consultation.

## Layout

- `build.py` generates every page. Page copy, services, contact details and navigation live here.
- `src/styles.css`, `src/site.js` are the shared stylesheet and script.
- `assets/` holds the logo and icons.

## Build locally

```sh
python3 build.py
```

This writes `dist/` (the deployable site) and `preview/` (used for previews). Both are git-ignored. Open `dist/index.html` in a browser to check it.

## Deploy

Every push to `main` runs `.github/workflows/deploy.yml`, which builds the site and deploys `dist/` plus the contact form function (`functions/api/contact.js`) to the Cloudflare Pages project `kts-website-staging`, which serves kickstarttechsolutions.com. You can also run it by hand from the Actions tab.

The workflow needs two repository secrets:

- `CLOUDFLARE_API_TOKEN` (Cloudflare Pages: Edit permission)
- `CLOUDFLARE_ACCOUNT_ID`
- `RESEND_API_KEY` (contact form email via Resend; copied into the Pages project as a secret on each deploy)

Staging lives at https://staging.kickstarttechsolutions.com and is protected by Cloudflare Access (only @focusdesignconsulting.com emails can sign in).

Never commit `.env` or any credentials.

## Contact form

`functions/api/contact.js` emails submissions to connect@kickstarttechsolutions.com via Resend (sender website@updates.kickstarttechsolutions.com). Cloudflare Turnstile protects it: the deploy workflow finds or creates the "KTS website contact form" widget, builds the site with its public site key, and stores its secret in Pages as `TURNSTILE_SECRET_KEY`.
