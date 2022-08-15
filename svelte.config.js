import adapter from '@sveltejs/adapter-auto';
import sveltePreprocess from 'svelte-preprocess';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		adapter: adapter(),
		// https://kit.svelte.dev/faq#aliases
		alias: {
			'assets': 'src/assets',
			'components': 'src/components',
			'data': 'src/data',
			'logic': 'src/logic',
			'routes': 'src/routes',
			'styles': 'src/styles',
		}

	},
	preprocess: sveltePreprocess(),
};

export default config;
