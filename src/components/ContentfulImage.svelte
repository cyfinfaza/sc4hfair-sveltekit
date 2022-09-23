<script>
	export let href = '';
	export let title = undefined;
	export let text = '';

	let isContentfulCdn = href.match(/^(https?:)?\/\/images.ctfassets.net\//),
		originalSrcset = [],
		webpSrcset = [],
		sizes =
			'(min-width: 768px) 640px, (min-width: 1024px) 960px, (min-width: 1500px) 1440px, (min-width: 1900px) 1920px 100vw';
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
