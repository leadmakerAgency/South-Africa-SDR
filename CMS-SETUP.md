# CMS Setup — Sveltia CMS (GitHub Backend)

The blog is managed via Sveltia CMS at `/admin/`. Content is stored as Markdown files in `content/posts/` and committed to GitHub.

## Prerequisites

1. Deploy the site with `npm run build` (outputs to `_site/`)
2. Ensure the site is accessible at `https://southafricasdr.com`

## GitHub OAuth App Setup

1. Go to **GitHub → Settings → Developer settings → OAuth Apps → New OAuth App**
2. Fill in:
   - **Application name:** South Africa SDR CMS
   - **Homepage URL:** `https://southafricasdr.com`
   - **Authorization callback URL:** `https://southafricasdr.com/admin/`
3. Copy the **Client ID** — Sveltia CMS will prompt for this on first login
4. Grant repo write access to editors on `leadmakerAgency/South-Africa-SDR`

## Editor Workflow

1. Open `https://southafricasdr.com/admin/`
2. Log in with GitHub (repo write access required)
3. Create or edit blog posts, upload featured images
4. Save → CMS commits `.md` + media to GitHub
5. Hosting rebuilds automatically → post appears at `/blog/[slug]/`

## Publishing Posts

- Set `draft: false` and `date` ≤ today to publish
- In production, drafts and future-dated posts are hidden automatically
- Local preview: `npm run dev` shows all posts including drafts

## Build Commands

```bash
npm install          # first time only
npm run dev          # local dev server with live reload
npm run build        # production build → _site/
```

## Netlify Alternative

If deploying to Netlify, you can use **Netlify Identity + Git Gateway** instead of direct GitHub OAuth. Enable Identity in Netlify dashboard and add the Git Gateway plugin.
