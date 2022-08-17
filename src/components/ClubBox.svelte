<script>
	import SvelteMarkdown from 'svelte-markdown';
	import LinkButton from 'components/LinkButton.svelte';
	import { interestsSlugs, removeInterest } from 'logic/supabase.js';
	export let club;
	let slugList = [];
</script>

<div class="clubEntry">
	<h2>{club.name}</h2>
	<SvelteMarkdown renderers={{ image: null }} source={club.description} />
	<div class="actionButtonsPanel">
		{#if club.tent}
			<LinkButton label="Map" icon="place" href={`/map?locate=${club.tent}`} lightFont />
		{/if}
		{#if ($interestsSlugs || []).indexOf(club.slug) > -1}
			<LinkButton
				label="Remove"
				icon="remove"
				on:click={(_) => removeInterest(club.slug)}
				lightFont
			/>
		{:else}
			<LinkButton label="Add" icon="add" href={`/interests?add=${club.slug}`} lightFont />
		{/if}
		<LinkButton label="View" icon="open_in_new" href={`/club/${club.slug}`} lightFont />
	</div>
</div>

<style>
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
	}

	.clubEntry > :global(*) {
		margin: 0;
	}

	.clubEntry > h2 {
		text-transform: uppercase;
	}

	.clubEntry > :global(p) {
		/* height: 64px; */
		width: calc(100% - var(--entry-padding) * 2);
		position: absolute;
	}

	.clubEntry > :global(p):before {
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
