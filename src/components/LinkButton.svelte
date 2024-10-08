<script>
	import { menuOpen } from 'logic/stores';
	import { createEventDispatcher } from 'svelte';

	import 'styles/button.css';

	/** @type {string | undefined} */
	export let label = undefined; // text displayed on button
	/** @type {string | undefined} */
	export let href = undefined; // navigates to a url, use on:click for custom js
	/** @type {string | undefined} */
	export let icon = undefined; // material icon name, use slot="iconElement" for a custom element
	export let header = false; // large header button (for main pages)
	export let headerSmall = false; // normal button size with header color
	export let noCloseHeader = false; // don't close the header when clicked
	export let acrylic = false; // translucent and blurred backdrop
	export let lightFont = false; // light font weight (not bold)
	export let disabled = false; // prevent click and navigation
	export let alert = false; // blinking yellow border
	export let active = false; // green background
	export let danger = false; // red background
	export let external = false; // open link in new tab
	/** @type {Record<string, any>} */
	export let props = {}; // additional props for the element
	let className = '';
	export { className as class }; // additional classes for the button element

	const dispatch = createEventDispatcher();

	let elementType = href ? 'a' : 'button';
	$: {
		if (elementType === 'a') {
			props.href = href;
			props.target = external ? '_blank' : null;
		} else {
			delete props.href;
			delete props.target;
		}
	}
	$: if (elementType === 'button' && !props.type) props.type = 'button';
	$: props.disabled = disabled ? true : undefined;
</script>

<svelte:element
	this={elementType}
	role="button"
	tabindex="0"
	on:click={(e) => {
		if (disabled) {
			e.preventDefault();
		} else {
			if ((header || headerSmall) && !noCloseHeader) $menuOpen = false;
			dispatch('click');
		}
	}}
	class={`container button ${className || ''}`}
	class:alert
	class:header
	class:headerSmall
	class:acrylic
	class:active
	class:danger
	{...props}
>
	{#if icon}
		<span class="material-icons icon" aria-hidden="true">{icon}</span>
	{:else}
		<div class="iconElementContainer">
			<slot name="iconElement" />
		</div>
	{/if}
	{#if label}
		<span class:lightFont={lightFont || headerSmall} class="label">{label}</span>
	{/if}
</svelte:element>

<style lang="scss">
	/* link button */
	.container {
		display: inline-flex;
		flex-direction: row;
		align-items: center;
		justify-content: center;
		text-align: center;
		padding: 8px;
		width: auto;
		margin: 0;
		border-radius: 8px;
		--linkbutton-icon-size: 24px;
		/* margin-inline-end: 8px; */
		/* margin-block-end: 8px; */
		user-select: none;
		&:not(.header) {
			gap: 4px;
		}
	}

	/* .container > *:not(.iconElementContainer) + * {
		margin-left: 4px !important;
	} */

	:global(a).container {
		text-decoration: none;
		color: unset;
	}

	.container .icon {
		width: var(--linkbutton-icon-size);
		height: var(--linkbutton-icon-size);
		font-size: var(--linkbutton-icon-size);
	}

	.container .label {
		margin: 0;
		padding: 0;
		font-size: 17px;
		font-weight: bold;
		letter-spacing: -0.7px;
		line-height: 1em;
		display: flex;
		/* transform: translateY(0.5px); */
	}

	.label.lightFont {
		font-weight: unset;
	}

	.container .iconElementContainer > :global(*) {
		fill: var(--text);
		width: var(--linkbutton-icon-size);
		height: var(--linkbutton-icon-size);
	}

	.iconElementContainer {
		display: flex;
		align-items: center;
		/* margin-right: 4px; */
	}

	/* header button */
	.header {
		width: 100px;
		height: 100px;
		border-radius: 8px;
		padding: 0;
		background-color: var(--navbar-accent);
		display: flex;
		flex-direction: column;
		align-items: center;
		text-align: center;
		justify-content: center;
		user-select: none;
	}

	.header .icon {
		font-size: 50px;
		width: 50px;
		height: 50px;
	}

	.header .label {
		margin: 0;
		font-size: 18px;
		font-weight: bold;
		letter-spacing: -0.7px;
		padding-inline: 8px;
		padding-right: 8px;
		padding-left: 8px;
		line-height: 1em;
		display: flex;
	}

	.headerSmall {
		background-color: var(--navbar-accent);
	}
</style>
