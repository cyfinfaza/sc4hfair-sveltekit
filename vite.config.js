import { sveltekit } from '@sveltejs/kit/vite';
import svg from '@poppanator/sveltekit-svg';

import { promisify } from 'util';
import { exec } from 'child_process';
const pexec = promisify(exec);
import { hostname } from 'os';

async function getInfo(env, cmd, length = false) {
	let value = process.env[env] || (await pexec(cmd)).stdout.trim();
	if (length) value = value.substring(0, length);
	return value;
}

const commit = await getInfo('VITE_VERCEL_GIT_COMMIT_SHA', 'git rev-parse --short HEAD', 7);
const buildTime = new Date();
export const versionKey = commit + '-' + buildTime.getTime().toString(36); // will be picked by sveltekit

/** @type {import('vite').UserConfig} */
const config = {
	define: {
		__COMMIT__: JSON.stringify(commit),
		__BRANCH__: JSON.stringify(
			await getInfo('VITE_VERCEL_GIT_COMMIT_REF', 'git rev-parse --abbrev-ref HEAD')
		),
		__BUILD_TIME__: JSON.stringify(buildTime.toISOString()),
		__BUILD_LOCATION__: JSON.stringify(
			(process.env.VERCEL && 'vercel') || process.env.BUILD_LOCATION_NAME || hostname()
		),
		__WEBPUSH_API_PREFIX__: JSON.stringify(process.env.WEBPUSH_API_PREFIX || ''), // needs a fallback
	},
	plugins: [sveltekit(), svg()],
	server: {
		proxy: {
			'/api/webpush': 'http://127.0.0.1:6002/',
		},
	},
	build: {
		sourcemap: true,
	},
};

export default config;
