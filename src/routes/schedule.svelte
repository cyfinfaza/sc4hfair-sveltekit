<script context="module">
	import { queryContentful } from 'logic/contentful.js';
	const query = `{
	scheduledEventCollection(order:sys_firstPublishedAt_DESC) {
		items {
			sys {
				id
			}
			title
			time
			tent
		}
	}
}`;
	export async function load({ fetch }) {
		const resp = await queryContentful(fetch, query);
		// console.log(resp);
		return { props: { events: resp.scheduledEventCollection?.items } };
	}
</script>

<script>
	import Layout from 'components/Layout.svelte';
	import tentSlugs from 'data/tentSlugs.json';
	import ToggleButton from 'components/ToggleButton.svelte';
	import EventBox, { eventIsFuture } from 'components/EventBox.svelte';
	import { exactSearch } from 'logic/search.js';
	export let events;
	// console.log(events);

	const eventTentsList = events.reduce(
		(last, current) => {
			if (last.indexOf(current.tent) < 0 && current.tent && current.tent !== '---') {
				return [...last, current.tent];
			}
			return last;
		},
		['All']
	);

	const isBrowser = typeof window !== 'undefined';

	let selectedTent = 'All';
	let showingPast = true;
	let searchQuery = '';
	let starredEvents = isBrowser ? JSON.parse(localStorage.getItem('starredEvents')) || [] : [];
	let showingOnlyStarredEvents = false;

	$: isBrowser && window.localStorage.setItem('starredEvents', JSON.stringify(starredEvents));

	function toggleStarredEvent(id) {
		if (starredEvents.includes(id)) {
			starredEvents = starredEvents.filter((event) => event !== id);
		} else {
			starredEvents = [...starredEvents, id];
		}
	}

	let results = [];
	$: results = exactSearch(
		events
			.filter(
				(element) =>
					((selectedTent === 'All' || selectedTent === element.tent) &&
						(eventIsFuture(element) || showingPast)) ||
					(isBrowser && window.location?.hash === '#' + element.id)
			)
			.map((element) => {
				return {
					...element,
					tentName: tentSlugs[element.tent] || element.tent,
					description: { description: element.description?.description || '' },
				};
			}),
		'title',
		['description', 'tentName'],
		searchQuery
	).filter((element) => !showingOnlyStarredEvents || starredEvents.includes(element.sys.id));
</script>

<Layout title="Schedule">
	<h1 class="center">Events</h1>
	<div class="filterOptions">
		<p>Filter:</p>
		<select bind:value={selectedTent} name="Tent">
			{#each eventTentsList as tent}
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
