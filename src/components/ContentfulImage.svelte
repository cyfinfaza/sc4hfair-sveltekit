<script>
	export let href = '';
	export let title = undefined;
	export let text = '';

	let isContentfulCdn = href.match(/^(https?:)?\/\/images.ctfassets.net\//),
		originalSrcset = [],
		webpSrcset = [],
		sizes = '(min-width: 1366px) 916px, (min-width: 1536px) 1030px, 100vw';
	if (isContentfulCdn) {
		for (let size of [640, 960, 1440, 1920]) {
			let img = `${href}?w=${size}`;
			originalSrcset.push(`${img} ${size}w`);
			webpSrcset.push(`${img}&fm=webp ${size}w`);
		}
	}
</script>

{#if isContentfulCdn}
	<picture>
		<source srcset={webpSrcset.join(',')} {sizes} type="image/webp" />
		<source srcset={originalSrcset.join(',')} {sizes} />
		<img {title} alt={text} src={href} />
	</picture>
{:else}
	<img src={href} {title} alt={text} />
{/if}
