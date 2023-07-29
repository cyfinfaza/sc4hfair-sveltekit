<script>
	import Layout from 'components/Layout.svelte';
	import tentSlugs from 'data/tentSlugs.json';
	import ToggleButton from 'components/ToggleButton.svelte';
	import EventBox from './EventBox.svelte';
	import { eventIsFuture } from 'logic/scheduling.js';
	import { exactSearch } from 'logic/search.js';
	import { browser } from '$app/environment';

	export let data;

	let selectedTent = 'All';
	let showingPast = false;
	let searchQuery = '';
	let starredEvents = (browser && JSON.parse(localStorage.getItem('starredEvents'))) || [];
	let showingOnlyStarredEvents = false;

	$: browser && window.localStorage.setItem('starredEvents', JSON.stringify(starredEvents));

	function toggleStarredEvent(id) {
		if (starredEvents.includes(id)) {
			starredEvents = starredEvents.filter((event) => event !== id);
		} else {
			starredEvents = [...starredEvents, id];
		}
	}

	let results = [];
	$: results = exactSearch(
		data.events
			.filter(
				(element) =>
					((selectedTent === 'All' || selectedTent === element.tent) &&
						(eventIsFuture(element) || showingPast)) ||
					(browser && window.location?.hash === '#' + element.id)
			)
			.map((element) => {
				return {
					...element,
					tentName: tentSlugs[element.tent] || element.tent,
				};
			}),
		'title',
		['tentName'],
		searchQuery
	).filter((element) => !showingOnlyStarredEvents || starredEvents.includes(element.sys.id));
</script>

<Layout title="Schedule">
	<h1 class="center">Events</h1>
	<div class="filterOptions">
		<p>Filter:</p>
		<select bind:value={selectedTent} name="Tent">
			{#each data.eventTentsList as tent}
				<option value={tent} key={tent}>
					{tentSlugs[tent] || tent}
				</option>
			{/each}
		</select>
		<input type="text" placeholder="Search" bind:value={searchQuery} />
		<ToggleButton bind:value={showingPast}>Show Past Events</ToggleButton>
		<ToggleButton bind:value={showingOnlyStarredEvents}>Show Only Starred Events</ToggleButton>
	</div>
	<div class="columnCentered">
		{#each results as event, i (event.sys.id)}
			<EventBox
				{event}
				index={i}
				starred={starredEvents.includes(event.sys.id)}
				{toggleStarredEvent}
			/>
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
</style>
