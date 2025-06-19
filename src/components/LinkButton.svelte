<script lang="ts">
	import { menuOpen } from 'logic/stores.svelte';
	import 'styles/button.css';
	import type {
		HTMLAnchorAttributes,
		HTMLButtonAttributes,
		MouseEventHandler,
	} from 'svelte/elements';

	type FullProps = HTMLAnchorAttributes & HTMLButtonAttributes;

	type Props = FullProps & {
		/** navigates to a url, use on:click for custom js */
		href?: string;
		/** click handler, use href for navigation */
		onclick?: MouseEventHandler<HTMLButtonElement>;

		/** text displayed on button */
		label?: string;
		/** material icon name, use slot="iconElement" for a custom element */
		icon?: string;

		acrylic?: boolean;
		/** light font weight (not bold) */
		lightFont?: boolean;
		/** prevent click and navigation */
		disabled?: boolean | null;

		/** background green/yellow/red */
		active?: boolean | 'warning' | 'danger';
		/** blinking yellow border */
		alert?: boolean;

		/** large header button (for main pages) */
		header?: boolean;
		/** normal button size with header color */
		headerSmall?: boolean;
		/** don't close the header when clicked */
		noCloseHeader?: boolean;
		/** translucent and blurred backdrop */

		/** open link in new tab */
		external?: boolean;

		iconElement?: import('svelte').Snippet;
	};

	let {
		label = undefined,
		href = undefined,
		onclick = undefined,
		icon = undefined,
		header = false,
		headerSmall = false,
		noCloseHeader = false,
		acrylic = false,
		lightFont = false,
		disabled = false,
		alert = false,
		active = false,
		external = false,
		iconElement,
		...additionalProps
	}: Props = $props();

	let elementType = $derived(href ? 'a' : 'button');

	let fullProps = $derived.by(() => {
		let p: FullProps = { ...additionalProps };

		if (elementType === 'a') {
			p.href = href;
			p.target = external ? '_blank' : null;
		} else {
			delete p.href;
			delete p.target;
		}

		if (elementType === 'button' && !p.type) p.type = 'button';

		p.disabled = disabled ? true : undefined;

		return p;
	});
</script>

<svelte:element
	this={elementType}
	role="button"
	tabindex="0"
	{...fullProps}
	onclick={(e) => {
		if (disabled) {
			e.preventDefault();
		} else {
			if ((header || headerSmall) && !noCloseHeader) $menuOpen = false;
			onclick?.(e);
		}
	}}
	class={`container button ${fullProps.class || ''}`}
	class:acrylic
	class:header
	class:headerSmall
	class:alert
	class:warning={active === 'warning'}
	class:danger={active === 'danger'}
	class:active={active === true}
>
	{#if icon}
		<span class="material-icons icon" aria-hidden="true">{icon}</span>
	{:else}
		<div class="iconElementContainer">
			{@render iconElement?.()}
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
