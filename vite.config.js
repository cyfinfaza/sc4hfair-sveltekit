import { sveltekit } from '@sveltejs/kit/vite';
import svelteSVG from 'vite-plugin-svelte-svg';

import { promisify } from 'util';
import { exec } from 'child_process';
const pexec = promisify(exec);
import { hostname } from 'os';

async function getInfo(env, cmd, length = false) {
	let value = process.env[env] || (await pexec(cmd)).stdout.trim();
	if (length) value = value.substring(0, length);
	return JSON.stringify(value);
}

/** @type {import('vite').UserConfig} */
const config = {
	define: {
		__COMMIT__: await getInfo('VITE_VERCEL_GIT_COMMIT_SHA', 'git rev-parse --short HEAD', 7),
		__BRANCH__: await getInfo('VITE_VERCEL_GIT_COMMIT_REF', 'git rev-parse --abbrev-ref HEAD'),
		__BUILD_TIME__: JSON.stringify(new Date().toISOString()),
		__BUILD_LOCATION__: JSON.stringify(process.env.BUILD_LOCATION_NAME || hostname()),
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
