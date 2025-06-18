import adapter from '@sveltejs/adapter-static';
import { sveltePreprocess } from 'svelte-preprocess';
import { versionKey } from './vite.config.js';

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
		version: {
			name: versionKey,
			// manually check every 5 minutes for updates
			// the browser will only check for a sw update on reload
			// but the user might leave the app open so we still want to get those updates
			pollInterval: 300000,
		},
	},
	preprocess: [
		sveltePreprocess({
			postcss: true,
		}),
	],
};

export default config;
