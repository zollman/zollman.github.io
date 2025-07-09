// @ts-check
import { defineConfig } from "astro/config";

import react from "@astrojs/react";
import tailwind from "@astrojs/tailwind";
import sitemap from "@astrojs/sitemap";

// Environment-based configuration
const getWebsiteUrl = () => {
    if (process.env.PUBLIC_WEBSITE_URL) {
        return process.env.PUBLIC_WEBSITE_URL;
    }
    
    // Default fallbacks based on environment
    if (process.env.ENVIRONMENT === 'staging') {
        return 'https://staging.yourdomain.com';
    } else if (process.env.ENVIRONMENT === 'production') {
        return 'https://yourdomain.com';
    }
    
    return 'http://localhost:4321';
};

const getBasePath = () => {
    return process.env.PUBLIC_BASE_PATH || '';
};

// https://astro.build/config
export default defineConfig({
    integrations: [react(), tailwind(), sitemap()],
    output: "static",
    site: getWebsiteUrl(),
    base: getBasePath(),
    vite: {
        define: {
            // Make environment variables available to the client
            'import.meta.env.PUBLIC_WEBSITE_URL': JSON.stringify(process.env.PUBLIC_WEBSITE_URL || getWebsiteUrl()),
            'import.meta.env.PUBLIC_BASE_PATH': JSON.stringify(process.env.PUBLIC_BASE_PATH || ''),
        }
    }
});
