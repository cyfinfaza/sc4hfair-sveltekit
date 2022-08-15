<script>
	import { createEventDispatcher } from 'svelte';
	import { menuOpen } from '../logic/stores';

	import '../styles/button.css';
	export let label = undefined;
	export let href = undefined;
	export let icon = undefined;
	export let iconStyle = undefined;
	export let header = false;
	export let acrylic = false;
	export let lightFont = false;
	export let disabled = false;
	export let alert = false;
	export let accent = false;

	const dispatch = createEventDispatcher();
	function onClick() {
		if(header) $menuOpen = false;
		dispatch('click')
	}
</script>

{#if href}
	<a
		{href}
		on:click={onClick}
		class="container button"
		class:alert
		class:header
		class:acrylic
		class:accent
	>
		{#if icon}
			<span class="material-icons icon" style={iconStyle}>{icon}</span>
		{:else}
			<slot name="iconElement" />
		{/if}
		{#if label}
			<span class:lightFont class="label">{label}</span>
		{/if}
	</a>
{:else}
	<button
		on:click={onClick}
		class="container button"
		class:alert
		class:header
		class:acrylic
		class:accent
	>
		{#if icon}
			<span class="material-icons icon" style={iconStyle}>{icon}</span>
		{:else}
			<slot name="iconElement" />
		{/if}
		{#if label}
			<span class:lightFont class="label">{label}</span>
		{/if}
	</button>
{/if}

<style>
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
	}

	.container > * + * {
		margin-left: 4px !important;
	}

	a.container {
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

	.container .iconElementContainer > * {
		fill: var(--text);
		width: var(--linkbutton-icon-size);
		height: var(--linkbutton-icon-size);
	}

	.iconElementContainer {
		display: flex;
		align-items: center;
		margin-right: 4px;
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
</style>
