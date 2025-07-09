# Cloudflare Workers Deployment Setup (Static Site)

This document explains how to deploy your static Astro site to Cloudflare Workers.

## Overview

This setup deploys your Astro site as a static site served by Cloudflare Workers. The configuration includes:

- **Static Output**: Your Astro site is built as static files
- **Worker Script**: A simple worker serves the static files with proper routing
- **No Sessions/KV**: Simplified configuration without database features
- **Environment Support**: Separate staging and production deployments

## Key Files

1. **`wrangler.toml`** - Cloudflare Workers configuration with static assets
2. **`worker.js`** - Simple worker script to serve static files with proper routing
3. **`astro.config.cloudflare.mjs`** - Astro config for static output (no adapter needed)
4. **`.github/workflows/deploy-cloudflare.yml`** - GitHub Actions for automated deployment

## Prerequisites

1. **Cloudflare Account**: You need a Cloudflare account with a domain configured
2. **Wrangler CLI**: Install globally with `npm install -g wrangler`
3. **GitHub Secrets**: Configure the following secrets in your GitHub repository

## Required GitHub Secrets

In your GitHub repository settings, add these secrets:

- `CLOUDFLARE_API_TOKEN`: Your Cloudflare API token with appropriate permissions
- `CLOUDFLARE_ACCOUNT_ID`: Your Cloudflare account ID

### Getting Your Cloudflare Credentials

1. **API Token**: 
   - Go to [Cloudflare Dashboard](https://dash.cloudflare.com/profile/api-tokens)
   - Create a custom token with these permissions:
     - Zone:Zone:Read
     - Zone:DNS:Edit  
     - Account:Cloudflare Workers:Edit

2. **Account ID**:
   - Go to your [Cloudflare Dashboard](https://dash.cloudflare.com/)
   - Copy the Account ID from the right sidebar

## Configuration Files

### wrangler.toml
The main configuration file for Cloudflare Workers. Update the following:

- Replace `"yourdomain.com"` with your actual domain
- Update the `routes` patterns to match your desired URLs
- Modify environment variables as needed

### astro.config.cloudflare.mjs
Astro configuration specifically for Cloudflare Workers deployment:

- Uses the `@astrojs/cloudflare` adapter
- Configures server-side rendering (SSR)
- Handles environment-specific URLs and base paths

## Build Commands

- `npm run build:cloudflare` - Build for Cloudflare Workers
- `npm run build:cloudflare:staging` - Build for staging environment
- `npm run build:cloudflare:production` - Build for production environment

## Local Development

1. Install Wrangler CLI: `npm install -g wrangler`
2. Login to Cloudflare: `wrangler login`
3. Use the deployment script: `./deploy-cloudflare.sh staging`

## Deployment

### Automatic Deployment (GitHub Actions)

The workflow `.github/workflows/deploy-cloudflare.yml` automatically deploys:

- **Staging**: When you push to `develop` branch (currently commented out)
- **Production**: When you push to `main` branch
- **Manual**: Using the GitHub Actions interface

### Manual Deployment

1. Build the project: `npm run build:cloudflare:staging`
2. Deploy with Wrangler: `wrangler deploy --env staging`

## Environment Variables

The deployment uses these environment variables:

- `ENVIRONMENT`: The target environment (staging/production)
- `PUBLIC_WEBSITE_URL`: The full URL where the site will be deployed
- `PUBLIC_BASE_PATH`: The base path for the site (usually empty for Workers)

## Different Base Paths

For Cloudflare Workers, you typically don't need a base path since each environment can have its own subdomain or domain. However, if you need different base paths:

1. Update the `PUBLIC_BASE_PATH` in `wrangler.toml`
2. Modify the GitHub Actions workflow to pass the correct base path
3. Ensure your Astro routes handle the base path correctly

## Troubleshooting

### Common Issues

1. **Build Failures**: Ensure all dependencies are installed with `npm ci`
2. **Environment Variables**: Check that all required env vars are set
3. **Domain Configuration**: Verify your Cloudflare DNS settings
4. **API Token Permissions**: Ensure your API token has the correct permissions

### Testing Locally

1. Build the project: `npm run build:cloudflare`
2. Use Wrangler dev: `wrangler dev`
3. Test your site at the provided local URL

## Next Steps

1. Update `wrangler.toml` with your actual domain names
2. Configure your GitHub repository secrets
3. Update the GitHub Actions workflow if needed
4. Test the deployment process
5. Set up monitoring and analytics in Cloudflare Dashboard
