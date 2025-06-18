<script>
	import Layout from 'components/Layout.svelte';
	import LinkButton from 'components/LinkButton.svelte';
	import { isOnline, kioskMode } from 'logic/stores';
	import { addInterest, initInterests, interestsSlugs, removeInterest } from 'logic/interests.js';
	import { canWebShare, share } from 'logic/webshare.js';
	import { onMount } from 'svelte';
	import SvelteMarkdown from 'svelte-markdown';

	/** @type {import('./$types').PageData} */
	export let data;
	const club = data.club;

	onMount(initInterests);
</script>

<Layout title={club.name}>
	<div
		class="horizPanel"
		style="whitespace: nowrap; justify-content: flex-start; margin-top: 16px;"
	>
		<LinkButton label="See all clubs" icon="groups" href="/clubs" />
		{#if !$kioskMode}
			<LinkButton label="View interest list" icon="list" href="/interests" disabled={!$isOnline} />
		{/if}
	</div>
	<h1 style="text-transform: uppercase;">
		{club.name}
		<div class="tags" style="text-transform: uppercase;">
			{#each club.tags || [] as tag}
				<div title={tag.toUpperCase()}>{tag}</div>
			{/each}
		</div>
	</h1>
	<div class="optionsButtonsPanel">
		{#if !$kioskMode}
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
		{/if}
		{#if club.tent}
			<LinkButton
				label="Locate at fair"
				icon="place"
				href={'/map/?locate=' + club.tent}
				lightFont
			/>
		{/if}
		{#if $canWebShare}
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
	{#if club.description}
		<div class="clubDescription">
			<SvelteMarkdown source={club.description} options={{ mangle: false }} />
		</div>
	{/if}
	{#if club.meetingLocation}<p><strong>Where:</strong> {club.meetingLocation}</p>{/if}
	{#if club.meetingWhen}<p><strong>When:</strong> {club.meetingWhen}</p>{/if}
	{#if club.grades}<p><strong>Grades:</strong> {club.grades}</p>{/if}
	{#if !$kioskMode && club.listingWebsite}
		<p><a href={club.listingWebsite}>View on 4histops.org</a></p>
	{/if}
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

	.tags > * {
		font-size: 0.5em;
	}
</style>
