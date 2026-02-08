---
description: Deploy the site to GitHub Pages and verify it works
---

# Deploy to GitHub Pages

Use this workflow to deploy the Vumbua wiki to GitHub Pages.

## Prerequisites
- Git repository initialized
- Remote origin configured to GitHub

## Steps

1. **Check git status**
   // turbo
   ```bash
   git status
   ```

2. **Stage all documentation changes**
   // turbo
   ```bash
   git add docs/ README.md .agent/
   ```

3. **Commit the changes**
   ```bash
   git commit -m "Update Vumbua campaign wiki"
   ```

4. **Push to GitHub**
   ```bash
   git push origin main
   ```

5. **Enable GitHub Pages (first time only)**
   - Go to repository Settings on GitHub
   - Navigate to Pages section
   - Set Source to: `main` branch, `/docs` folder
   - Save

6. **Verify deployment**
   - Wait 1-2 minutes for GitHub Actions to build
   - Visit: `https://[username].github.io/vumbua/`
   - Check that pages render correctly

## Troubleshooting

### Site not updating
- Check GitHub Actions tab for build errors
- Ensure `_config.yml` is valid YAML
- Clear browser cache

### 404 errors on pages
- Check file paths match links exactly
- Ensure files have `.md` extension
- Verify frontmatter is valid

### Theme not applying
- Check `theme` in `_config.yml`
- Ensure theme name is exact (e.g., `jekyll-theme-cayman`)

## Configuration Reference

The site config is at `docs/_config.yml`:
```yaml
title: Vumbua Campaign
theme: jekyll-theme-cayman
exclude:
  - gm-notes/  # Hidden from public site
```
