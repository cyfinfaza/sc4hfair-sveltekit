<script>
	import SvelteMarkdown from 'svelte-markdown';
	import DateTime from 'components/DateTime.svelte';
	import ContentfulImage from 'components/ContentfulImage.svelte';

	export let data;
	export let index = 0;
</script>

<div class="container" style:animation-delay={index * 0.1 + 's'}>
	<h3 class="title">{data.title}</h3>
	<SvelteMarkdown
		source={data.contentText}
		renderers={{ image: ContentfulImage }}
		options={{ mangle: false }}
	/>
	<DateTime date={data.sys.publishedAt} fromNow withTitle />
</div>

<style lang="scss">
	.container {
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
