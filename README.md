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

Every push to `main` runs `.github/workflows/deploy.yml`, which builds the site and deploys `dist/` to the Cloudflare Pages project `kts-website-staging`. You can also run it by hand from the Actions tab.

The workflow needs two repository secrets:

- `CLOUDFLARE_API_TOKEN` (Cloudflare Pages: Edit permission)
- `CLOUDFLARE_ACCOUNT_ID`

Staging lives at https://staging.kickstarttechsolutions.com and is protected by Cloudflare Access (only @focusdesignconsulting.com emails can sign in).

Never commit `.env` or any credentials.
