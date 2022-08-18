import adapter from '@sveltejs/adapter-static';
import sveltePreprocess from 'svelte-preprocess';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		adapter: adapter({
			pages: 'build',
			assets: 'build',
		}),
		// https://kit.svelte.dev/faq#aliases
		alias: {
			assets: 'src/assets/*',
			components: 'src/components/*',
			data: 'src/data/*',
			logic: 'src/logic/*',
			routes: 'src/routes/*',
			styles: 'src/styles/*',
		},
		prerender: {
			default: true,
		},
	},
	preprocess: [
		sveltePreprocess({
			postcss: true,
		}),
	],
};

export default config;
