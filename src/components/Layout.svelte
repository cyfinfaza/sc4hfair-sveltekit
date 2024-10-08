<script>
	import Header from 'components/Header.svelte';
	import { kioskMenuSize, kioskMode, menuOpen } from 'logic/stores';
	import { quintIn, quintOut } from 'svelte/easing';
	import { fly } from 'svelte/transition';
	import KioskMenu from './KioskMenu.svelte';

	export let title = '';
	export let description = 'The Somerset County 4‑H Fair App';
	export let noPadding = false;
	export let noHeaderPadding = false;
	export let fixedHeightContent = false;
	export let fullWidth = false;
	/** @type {string | undefined} */
	export let forceTheme = undefined;

	const SITE_NAME = 'Somerset County 4‑H Fair';
	const AUTHOR = 'Somerset County 4‑H';
	const animationDuration = 150;

	/** @type {string} */
	let kioskSizeString;
	/** @type {string} */
	let contentSizeString;
	$: {
		kioskSizeString = $kioskMenuSize + '%';
		contentSizeString = 100 - $kioskMenuSize + '%';
	}
</script>

<svelte:window
	on:keydown={(e) => {
		if (e.key === 'm' && (e.ctrlKey || e.metaKey))
			/** @type {HTMLElement} */ (
				document.querySelector('#menuArea :is(input, button, a)')
			)?.focus();
	}}
/>

<svelte:head>
	<title>{title ? title + ' | ' : ''} {SITE_NAME}</title>
	<meta name="description" content={description} />
	<meta property="og:title" content={title} />
	<meta property="og:description" content={description} />
	<meta property="og:type" content="website" />
	<meta name="twitter:card" content="summary" />
	<meta name="twitter:creator" content={AUTHOR} />
	<meta name="twitter:title" content={title} />
	<meta name="twitter:description" content={description} />
	<meta name="theme-color" content="#009959" />
</svelte:head>

<a href="#content" class="skipToContentButton" tabindex="0" on:click={() => ($menuOpen = false)}>
	Skip to content <br />
	<span style="text-decoration: none; display: inline-block;">
		Using keyboard navigation? Use <kbd>Ctrl</kbd>+<kbd>M</kbd> or <kbd>Cmd</kbd>+<kbd>M</kbd> to quickly
		open the menu.
	</span>
</a>
<Header offsetContent={!noHeaderPadding && !fixedHeightContent} />
<noscript>JavaScript is required to use this app.</noscript>
{#key title}
	<div
		in:fly|global={{
			duration: animationDuration,
			delay: animationDuration,
			y: 50,
			easing: quintOut,
		}}
		out:fly|global={{
			duration: animationDuration,
			y: -50,
			easing: quintIn,
		}}
		class={['content', forceTheme ? 'global-theme-' + forceTheme : null].filter(Boolean).join(' ')}
		id="content"
		class:noPadding
		class:fixedHeightContent
		class:kioskMode={$kioskMode}
		style:width={$kioskMode ? contentSizeString : undefined}
		on:focusin={() => ($menuOpen = false)}
	>
		<div class:fullWidth>
			<slot />
		</div>
	</div>
{/key}
{#if $kioskMode}
	<div class="kioskBar" style:width={$kioskMode ? kioskSizeString : undefined}><KioskMenu /></div>
{/if}

<style lang="scss">
	.content {
		padding: 8px;
		width: 100%;
		box-sizing: border-box;
		pointer-events: painted;
		display: flex;
		justify-content: center;
		scroll-margin-top: calc(var(--nav-height) + 16px);
		padding-top: 0;
	}

	.content.noPadding {
		padding: 0 !important;
	}
	.content.fixedHeightContent {
		/* height: 100vh; */
		overflow: hidden;

		position: absolute;
		inset: 0;
	}

	.kioskBar {
		position: fixed;
		height: 100%;
		width: 30%;
		box-sizing: border-box;
		background: var(--bg);
	}

	.content.kioskMode {
		position: absolute;
		right: 0;
		width: 70%;
		box-sizing: border-box;
		padding: 1em;
		&.fixedHeightContent {
			right: 0;
			top: 0;
			bottom: 0;
			left: unset;
		}
	}

	.content > div.fullWidth {
		width: 100%;
		max-width: unset;
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
		z-index: 1000;
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
