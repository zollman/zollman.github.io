// Modern Cloudflare Worker for static Astro site
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // Handle root path
    if (url.pathname === '/') {
      return env.ASSETS.fetch(new URL('/index.html', url.origin));
    }
    
    // Handle directory paths by appending index.html
    if (url.pathname.endsWith('/')) {
      return env.ASSETS.fetch(new URL(url.pathname + 'index.html', url.origin));
    }
    
    // For paths without file extensions, try the exact path first, then with /index.html
    if (!url.pathname.includes('.')) {
      // Try the exact path first
      try {
        const response = await env.ASSETS.fetch(request);
        if (response.status === 200) {
          return response;
        }
      } catch (e) {
        // If that fails, try with /index.html
      }
      
      // Try with /index.html appended
      try {
        return env.ASSETS.fetch(new URL(url.pathname + '/index.html', url.origin));
      } catch (e) {
        // If that also fails, fall through to regular asset serving
      }
    }
    
    // For everything else, try to serve the asset directly
    try {
      return env.ASSETS.fetch(request);
    } catch (e) {
      // If asset not found, serve 404 page
      try {
        const notFoundResponse = await env.ASSETS.fetch(new URL('/404.html', url.origin));
        return new Response(notFoundResponse.body, {
          status: 404,
          statusText: 'Not Found',
          headers: notFoundResponse.headers,
        });
      } catch (e) {
        return new Response('Not Found', { 
          status: 404,
          headers: { 'Content-Type': 'text/plain' }
        });
      }
    }
  },
};
