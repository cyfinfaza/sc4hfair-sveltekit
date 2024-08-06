<script>
	import ContentfulImage from 'components/ContentfulImage.svelte';
	import DateTime from 'components/DateTime.svelte';
	import SvelteMarkdown from 'svelte-markdown';

	/** @type {{ title: string; contentText: string; sys: { publishedAt: string } }} */
	export let data;
	export let index = 0;
</script>

<article style:animation-delay={index * 0.1 + 's'}>
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
