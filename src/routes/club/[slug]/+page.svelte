<script>
	import Layout from 'components/Layout.svelte';
	import LinkButton from 'components/LinkButton.svelte';
	import { canWebShare, share } from 'logic/webshare.js';
	import { isOnline } from 'logic/stores';
	import SvelteMarkdown from 'svelte-markdown';
	import {
		interestsSlugs,
		addInterest,
		removeInterest,
		initSupabaseClient,
	} from 'logic/supabase.js';
	import { onMount } from 'svelte';

	/** @type {import('./$types').PageData} */
	export let data;
	const club = data.club;

	onMount(async () => {
		await initSupabaseClient();
	});
</script>

<Layout title={club.name}>
	<div
		class="horizPanel"
		style="whitespace: nowrap; justify-content: flex-start; margin-top: 16px;"
	>
		<LinkButton label="See all clubs" icon="groups" href="/clubs" />
		<LinkButton label="View interest list" icon="list" href="/interests" disabled={!$isOnline} />
	</div>
	<h1 style="text-transform: uppercase;">{club.name}</h1>
	<div class="optionsButtonsPanel">
		{#if ($interestsSlugs || []).includes(club.slug)}
			<LinkButton
				label="Remove from interest list"
				disabled={!$isOnline}
				icon="remove"
				on:click={() => removeInterest(club.slug)}
				lightFont
			/>
		{:else}
			<LinkButton
				label="Add to interest list"
				disabled={!$isOnline}
				icon="add"
				on:click={() => addInterest(club.slug)}
				lightFont
			/>
		{/if}
		{#if club.tent}
			<LinkButton
				label="Locate at fair"
				icon="place"
				href={'/map/?locate=' + club.tent}
				lightFont
			/>
		{/if}
		{#if canWebShare()}
			<LinkButton
				label="Share"
				icon="share"
				on:click={() => share(`${club.name}`, window.location.href)}
				lightFont
			/>
		{/if}
		{#if club.clubWebsite}
			<LinkButton label="Website" icon="language" href={club.clubWebsite} lightFont />
		{/if}
	</div>
	<div class="clubDescription">
		<SvelteMarkdown source={club.description} options={{ mangle: false }} />
	</div>
	<p><strong>Where:</strong> {club.meetingLocation}</p>
	<p><strong>When:</strong> {club.meetingWhen}</p>
	<p><strong>Grades:</strong> {club.grades}</p>
	<p><a href={club.listingWebsite}>View on 4histops.org</a></p>
</Layout>

<style>
	.optionsButtonsPanel {
		display: flex;
		gap: 8px;
		margin-bottom: 8px;
		flex-wrap: wrap;
	}
	.optionsButtonsPanel > :global(*) {
		margin: 0 !important;
	}

	.clubDescription :global(img) {
		width: 100%;
		height: auto;
	}
</style>
