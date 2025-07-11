// Environment-based configuration helpers
const getWebsiteUrl = () => {
	// Check for explicit environment variable first
	if (import.meta.env.PUBLIC_WEBSITE_URL) {
		return import.meta.env.PUBLIC_WEBSITE_URL;
	}
	
	// Fallback based on build environment
	if (import.meta.env.PROD) {
		return 'https://sigsegv.com';
	}
	
	// Default for development
	return 'http://localhost:4321';
};

const getBasePath = () => {
	return import.meta.env.PUBLIC_BASE_PATH || '';
};

export const profile = {
	fullName: 'Aaron Zollman',
	title: 'Security nerd and software engineer. Fixing leaky abstractions in systems and organizations.',
	institute: '',
	author_name: 'Aaron Zollman', // Author name to be highlighted in the papers section
	research_areas: [
		// { title: 'Physics', description: 'Brief description of the research interest', field: 'physics' },
	],
}

// Set equal to an empty string to hide the icon that you don't want to display
export const social = {
	email: '',
	instagram: 'https://instagram.com/aaronzollman',
	linkedin: 'https://linkedin.com/in/zollman',
	x: 'https://www.x.com/aaronzollman',
	github: 'https://github.com/zollman',
	gitlab: '',
	scholar: '',
	inspire: '',
	arxiv: '',
}

export const template = {
	website_url: getWebsiteUrl(), // Astro needs to know your site’s deployed URL to generate a sitemap. It must start with http:// or https://
	menu_left: false,
	transitions: true,
	lightTheme: 'light', // Select one of the Daisy UI Themes or create your own
	darkTheme: 'dark', // Select one of the Daisy UI Themes or create your own
	excerptLength: 200,
	postPerPage: 5,
    base: getBasePath() // Repository name starting with /
}

export const seo = {
	default_title: 'Aaron Zollman - Security Nerd and Software Engineer',
	default_description: 'Personal website, with thoughts on security and software',
	default_image: '/assets/profile_pictures.jpg',
}
