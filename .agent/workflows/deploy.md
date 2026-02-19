---
description: Deploy the site to Netlify and verify it works
---

# Deploy to Netlify

Use this workflow to deploy the Vumbua wiki to Netlify.

## First-Time Setup

1. **Go to Netlify**
   - Visit https://app.netlify.com/
   - Sign up/login with GitHub

2. **Create new site**
   - Click "Add new site" → "Import an existing project"
   - Choose GitHub and select `ldstrebel/vumbua`
   - Netlify will auto-detect `netlify.toml` config

3. **Deploy settings** (auto-configured by netlify.toml)
   - Publish directory: `meta/docs/`
   - No build command needed (static files)

4. **Click Deploy**
   - Wait 1-2 minutes
   - Your site will be at: `https://[random-name].netlify.app`

5. **Optional: Custom domain**
   - Site settings → Domain management → Add custom domain

## Ongoing Deployments

After initial setup, Netlify auto-deploys on every push:

// turbo-all
```bash
git add index.md characters/ sessions/ factions/ world/ locations/ bestiary/ glossary.md timeline.md knowledge-tracker.md CHANGELOG.md meta/docs/ netlify.toml

git commit -m "Update campaign wiki"

git push
```

Netlify will automatically rebuild within 1-2 minutes.

## Troubleshooting

### Site not updating
- Check Netlify dashboard for deploy status
- Look at deploy logs for errors

### 404 on pages
- Ensure file paths match exactly
- Check that markdown files have `.md` extension

### Custom domain issues
- Add CNAME record pointing to Netlify
- Enable HTTPS in Netlify settings
