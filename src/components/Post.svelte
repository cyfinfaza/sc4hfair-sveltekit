<script context="module">
	/** @typedef {{ title: string; contentText: string; sys: { id: string; publishedAt: string } }} Post */
</script>

<script>
	import { browser } from '$app/environment';
	import ContentfulImage from 'components/ContentfulImage.svelte';
	import DateTime from 'components/DateTime.svelte';
	import { onMount, tick } from 'svelte';
	import SvelteMarkdown from 'svelte-markdown';

	/** @type {Post} */
	export let data;
	export let index = 0;

	/** @type {HTMLElement} */
	let article;
	onMount(async () => {
		await tick();
		if (browser && window.location?.hash === '#' + data.sys?.id) {
			article.scrollIntoView({ behavior: 'instant' });
		}
	});
</script>

<article bind:this={article} style:animation-delay={index * 0.1 + 's'} id={data.sys?.id}>
	<h3 class="title">{data.title}</h3>
	<SvelteMarkdown
		source={data.contentText}
		renderers={{ image: ContentfulImage }}
		options={{ mangle: false }}
	/>
	<DateTime date={data.sys.publishedAt} fromNow withTitle />
</article>

<style lang="scss">
	article {
		width: 100%;
		border-radius: 8px;
		background-color: var(--light);
		padding: 12px;
		margin-bottom: 16px;
		box-sizing: border-box;
		animation: zoomin 0.5s backwards ease;
		scroll-margin-top: 16px;

		& :global(img) {
			width: 100%;
			border-radius: 4px;
		}

		& :global(time) {
			opacity: 0.75;
			font-size: smaller;
		}

		& > *:last-child {
			margin-bottom: 0;
		}
	}

	.title {
		margin: 0;
		text-align: center;
		font-size: 1.25em;
	}

	@keyframes zoomin {
		0% {
			transform: scale(0.88);
			opacity: 0;
		}
	}
</style>
