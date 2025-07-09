#!/bin/bash

# Script to deploy to Cloudflare Workers with different environments

set -e

ENVIRONMENT=${1:-staging}

echo "Building for Cloudflare Workers ($ENVIRONMENT environment)..."

# Set environment variables based on the target environment
if [ "$ENVIRONMENT" = "production" ]; then
    export PUBLIC_WEBSITE_URL="https://yourdomain.com"
    export PUBLIC_BASE_PATH=""
elif [ "$ENVIRONMENT" = "staging" ]; then
    export PUBLIC_WEBSITE_URL="https://staging.yourdomain.com"
    export PUBLIC_BASE_PATH=""
else
    echo "Unknown environment: $ENVIRONMENT"
    echo "Usage: $0 [staging|production]"
    exit 1
fi

export ENVIRONMENT=$ENVIRONMENT

# Build the project
npm run build:cloudflare

echo "Build complete for $ENVIRONMENT environment"
echo "Website URL: $PUBLIC_WEBSITE_URL"
echo "Base Path: $PUBLIC_BASE_PATH"

# Optionally deploy with wrangler
if command -v wrangler &> /dev/null; then
    echo "Do you want to deploy to Cloudflare Workers? (y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo "Deploying to Cloudflare Workers..."
        wrangler deploy --env $ENVIRONMENT
    fi
else
    echo "Wrangler CLI not found. Install it with: npm install -g wrangler"
    echo "Then run: wrangler deploy --env $ENVIRONMENT"
fi
