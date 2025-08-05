<script>
	import { browser } from '$app/environment';
	import FourH from 'assets/4h.svg?component';
	import ClubBox from 'components/ClubBox.svelte';
	import Layout from 'components/Layout.svelte';
	import LinkButton from 'components/LinkButton.svelte';
	import { exactSearch } from 'logic/search.js';
	import { isOnline, kioskMode } from 'logic/stores.js';

	export let data;

	let searchQuery = (browser && window.sessionStorage.getItem('clubs_searchQuery')) || '';
	$: if (browser) window.sessionStorage.setItem('clubs_searchQuery', searchQuery);

	let results = [];
	$: results = exactSearch(searchQuery, data.clubs, 'name', [
		'description',
		'meetingWhen',
		'meetingLocation',
		'grades',
		'tags',
	]);
</script>

<Layout title="Clubs">
	<div class="center">
		<h1>Clubs</h1>
		{#if !$kioskMode}
			<p>Tap the +Add button to add a club to your interest list.</p>
			<p class="horizPanel">
				<LinkButton
					disabled={!$isOnline}
					icon="list_alt"
					label="View interest list"
					href="/interests"
				/>
				<LinkButton disabled={!$isOnline} label="Join 4‑H" href="https://4histops.org/membership">
					<svelte:fragment slot="iconElement">
						<FourH
							style="height: 100%; fill: currentColor; transition: fill var(--theme-transition);"
						/>
					</svelte:fragment>
				</LinkButton>
			</p>
		{/if}
	</div>
	<div class="filterOptions">
		<input type="text" placeholder="Search" bind:value={searchQuery} />
		<button style:display={searchQuery ? null : 'none'} on:click={() => (searchQuery = '')}
			>Clear</button
		>
	</div>
	<div class="columnCentered">
		{#each results as club}
			<ClubBox {club} autoTarget={browser && window.location?.hash === '#' + club.slug} />
		{/each}
	</div>
</Layout>

<style>
	.filterOptions {
		width: 100%;
		display: flex;
		justify-content: center;
		margin-bottom: 16px;
		align-items: center;
		gap: 8px;
		flex-wrap: wrap;
	}

	.filterOptions > * {
		margin-block: 0;
	}

	.filterOptions input {
		width: 250px;
		text-indent: 4px;
	}
</style>
