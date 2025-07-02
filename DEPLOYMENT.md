# Deployment Guide

This repository is configured to support multiple deployment options for the MKdocs documentation site.

## Vercel Deployment (Recommended)

The repository is now configured to deploy directly to Vercel with automatic builds:

### Setup
1. Connect your GitHub repository to Vercel
2. Vercel will automatically detect the configuration and build the site
3. The site will be built using the `mkdocs build` command defined in `package.json`
4. Static files will be served from the `site/` directory

### Configuration Files
- `requirements.txt`: Python dependencies needed for MKdocs
- `package.json`: Build scripts for Vercel
- `vercel.json`: Vercel-specific configuration with Python build commands
- `mkdocs.yml`: MKdocs configuration

### How Vercel Build Works
1. `installCommand`: Installs Python dependencies from requirements.txt
2. `buildCommand`: Runs `mkdocs build` to generate static files
3. `outputDirectory`: Serves files from the generated `site/` directory

### Automatic Deployments
- **Production**: Pushes to `main` branch will deploy to production
- **Preview**: Pushes to other branches will create preview deployments

## GitHub Pages Deployment (Legacy)

The existing GitHub Pages deployment via the `cd.yml` workflow will continue to work:
- Triggered on tag pushes (e.g., `v1.0.0`)
- Builds and deploys to `gh-pages` branch
- Available at the domain specified in `docs/CNAME`

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Serve locally
mkdocs serve

# Build static files
mkdocs build
```

## Domain Configuration

The site is configured to use the custom domain `auto-optional.daanluttik.nl` via:
- `docs/CNAME` file for GitHub Pages
- Domain settings in Vercel dashboard for Vercel deployment

Choose your preferred deployment method and configure the domain accordingly in the respective platform's dashboard.