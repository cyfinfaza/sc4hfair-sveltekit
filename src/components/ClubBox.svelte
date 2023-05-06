<script>
	import SvelteMarkdown from 'svelte-markdown';
	import LinkButton from 'components/LinkButton.svelte';
	import { isOnline } from 'logic/stores.js';
	import { interestsSlugs, removeInterest } from 'logic/supabase.js';
	import { onMount, tick } from 'svelte';

	export let club;
	let slugList = [];

	export let autoTarget = false;
	/** @type {HTMLDivElement} */
	let div;
	onMount(async () => {
		await tick();
		if (autoTarget) {
			div.scrollIntoView();
			window.div = div;
		}
	});
</script>

<div class="clubEntry" id={club.slug} class:targeted={autoTarget} bind:this={div}>
	<h2>{club.name}</h2>
	<SvelteMarkdown renderers={{ image: null }} source={club.description} />
	<div class="actionButtonsPanel">
		{#if club.tent}
			<LinkButton label="Map" icon="place" href={`/map?locate=${club.tent}`} lightFont />
		{/if}
		{#if ($interestsSlugs || []).indexOf(club.slug) > -1}
			<LinkButton
				label="Remove"
				disabled={!$isOnline}
				icon="remove"
				on:click={(_) => removeInterest(club.slug)}
				lightFont
			/>
		{:else}
			<LinkButton
				label="Add"
				disabled={!$isOnline}
				icon="add"
				href={`/interests?add=${club.slug}`}
				lightFont
			/>
		{/if}
		<LinkButton label="View" icon="open_in_new" href={`/club/${club.slug}`} lightFont />
	</div>
</div>

<style lang="scss">
	.clubEntry {
		width: 100%;
		border-radius: 8px;
		background-color: var(--light);
		--entry-padding: 12px;
		padding: var(--entry-padding);
		margin-bottom: 16px;
		overflow: hidden;
		position: relative;
		box-sizing: border-box;

		&.targeted {
			border: 2px solid var(--accent);
		}

		> :global(*) {
			margin: 0;
		}

		> h2 {
			text-transform: uppercase;
		}

		> :global(p) {
			/* height: 64px; */
			width: calc(100% - var(--entry-padding) * 2);
			position: absolute;
		}

		> :global(p):before {
			content: '';
			width: 100%;
			height: 100%;
			position: absolute;
			left: 0;
			top: 0;
			background: linear-gradient(transparent 20px, var(--light) 98px);
			/* TODO make this also have a nice transition */
			transition: background var(--theme-transition);
		}
	}

	.actionButtonsPanel {
		margin-top: 48px;
		display: flex;
		width: 100%;
		justify-content: flex-end;
		z-index: 20;
		position: relative;
		gap: 8px;
	}
</style>
