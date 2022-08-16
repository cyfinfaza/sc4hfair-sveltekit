<script context="module">
	import { getClubs } from 'logic/contentful.js';
	export async function load({ fetch }) {
		const resp = await getClubs(fetch);
		// console.log(resp);
		return { props: { clubs: resp } };
	}
</script>

<script>
	import { page } from '$app/stores';
	import Layout from 'components/Layout.svelte';
	import LinkButton from 'components/LinkButton.svelte';
	import { canWebShare, share } from 'logic/webshare';
	import SvelteMarkdown from 'svelte-markdown';
	import {
		interestsSlugs,
		addInterest,
		removeInterest,
		initSupabaseClient,
	} from 'logic/supabase.js';
	import { onMount } from 'svelte';

	export let clubs;

	const isBrowser = typeof window !== 'undefined';
	const slug = $page.params.slug;
	const club = clubs.find((club) => club.slug === slug);

	onMount(async () => {
		await initSupabaseClient();
	});
</script>

<Layout title={club.name}>
	<div
		class="horizPanel"
		style="whitespace: nowrap; justify-content: flex-start; margin-top: 16px;"
	>
		<LinkButton label="See all clubs" icon="groups" href="/clubs" inline />
		<LinkButton label="View interest list" icon="list" href="/interests" inline />
	</div>
	<h1 style="text-transform: uppercase;">{club.name}</h1>
	<div class="optionsButtonsPanel">
		{#if ($interestsSlugs || []).includes(club.slug)}
			<LinkButton
				label="Remove from interest list"
				icon="remove"
				on:click={() => removeInterest(club.slug)}
				lightFont
			/>
		{:else}
			<LinkButton
				label="Add to interest list"
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
		{#if isBrowser && canWebShare()}
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
		<SvelteMarkdown source={club.description} />
	</div>
	<p>
		<strong>Where: </strong>
		{club.meetingLocation}
	</p>
	<p>
		<strong>When: </strong>
		{club.meetingWhen}
	</p>
	<p>
		<strong>Grades: </strong>
		{club.grades}
	</p>
	<p>
		<a href={club.listingWebsite}>View on 4histops.org</a>
	</p>
</Layout>

<style>
	.optionsButtonsPanel {
		display: flex;
		gap: 8px;
		margin-bottom: 8px;
	}
	.optionsButtonsPanel > :global(*) {
		margin: 0 !important;
	}

	.clubDescription :global(img) {
		width: 100%;
		height: auto;
	}
</style>
