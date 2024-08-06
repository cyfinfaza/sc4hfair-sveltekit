/** @type {import('@sveltejs/kit').HandleClientError} */
export function handleError({ error, message }) {
	console.log(error, message);
	return {
		// @ts-expect-error
		name: error?.name || 'Error',
		// @ts-expect-error
		message: error?.message || message || '',
		// @ts-expect-error
		stack: error?.stack?.replace(/ {4}/g, '\t'),
	};
}
