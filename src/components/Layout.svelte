<script>
	import Header from './Header.svelte';

	export let title = '';
	export let description = '';
	export let noPadding = false;
	export let noHeaderPadding = false;
	export let fixedHeightContent = false;
	export let fullWidth = false;

	const SITE_NAME = 'Somerset County 4-H Fair';
	const DESCRIPTION = 'The Somerset County 4-H Fair App';
	const AUTHOR = 'Somerset County 4-H';
	const metaDescription = description || DESCRIPTION;
</script>

<svelte:head>
	<title>{title ? title + ' | ' : ''} {SITE_NAME}</title>
	<meta name="description" content={metaDescription} />
	<meta property="og:title" content={title} />
	<meta property="og:description" content={metaDescription} />
	<meta property="og:type" content="website" />
	<meta name="twitter:card" content="summary" />
	<meta name="twitter:creator" content={AUTHOR || ''} />
	<meta name="twitter:title" content={title} />
	<meta name="twitter:description" content={metaDescription} />
	<meta name="theme-color" content="#009959" />
</svelte:head>

<a href="#content" class="skipToContentButton">Skip to content</a>
<Header offsetContent={!noHeaderPadding && !fixedHeightContent} />
<div
	class="content"
	id="content"
	class:noPadding
	class:padTop={fixedHeightContent && !noHeaderPadding}
	class:fixedHeightContent
>
	<div class:fullWidth>
		<slot />
	</div>
</div>

<style>
	.content {
		padding: 8px;
		width: 100%;
		box-sizing: border-box;
		pointer-events: painted;
		display: flex;
		justify-content: center;
		scroll-margin-top: calc(var(--navbar-height) + 16px);
		padding-top: 0;
	}

	.content.noPadding {
		padding: 0;
	}
	.content.padTop {
		padding-top: var(--navbar-height);
	}
	.content.fixedHeightContent {
		height: 100vh;
		overflow: hidden;
	}

	.content > div.fullWidth {
		width: unset;
	}

	.content > div {
		width: 100%;
		max-width: 800px;
	}
	.skipToContentButton {
		position: fixed;
		top: 0;
		width: 100%;
		text-align: center;
		z-index: 200;
		padding: 8px;
		background-color: var(--light);
		color: var(--text);
		transform: translateY(-100%);
		transition: 240ms ease;
	}

	.skipToContentButton:focus {
		transform: none;
	}
</style>
