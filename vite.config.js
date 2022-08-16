import { sveltekit } from '@sveltejs/kit/vite';
import svelteSVG from 'vite-plugin-svelte-svg';

import { promisify } from 'util';
import { exec } from 'child_process';
const pexec = promisify(exec);

const version = JSON.stringify((await pexec('git rev-parse --short HEAD')).stdout.trim());

/** @type {import('vite').UserConfig} */
const config = {
	define: {
		__VERSION__: version,
	},
	plugins: [
		sveltekit(),
		svelteSVG({
			svgoConfig: {}, // See https://github.com/svg/svgo#configuration
			requireSuffix: false, // Set false to accept '.svg' without the '?component'
		}),
	],
};

export default config;
