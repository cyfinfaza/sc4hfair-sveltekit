<script context="module">
	import { queryContentful } from 'logic/contentful.js';
	const query = `{
	postCollection(order:sys_firstPublishedAt_DESC) {
		items {
			title
			contentText
			sys {
				publishedAt
			}
		}
	}
}`;
	export async function load({ fetch }) {
		return { props: { posts: (await queryContentful(fetch, query)).postCollection?.items } };
	}
</script>

<script>
	import LinkButton from 'components/LinkButton.svelte';
	import Layout from 'components/Layout.svelte';
	import Post from 'components/Post.svelte';
	import { theme } from 'logic/theming.js';
	import { menuOpen } from 'logic/stores.js';
	export let posts;
</script>

<Layout title="Home">
	<h1 class="center">Welcome to the Somerset County 4-H Fair.</h1>
	<button on:click={() => ($theme = 'dark')}>Dark</button>
	<button on:click={() => ($theme = 'light')}>Light</button>
	<div class="horizPanel">
		<LinkButton label="Schedule" icon="event_note" href="/schedule" />
		<LinkButton label="Map" icon="map" href="/map" />
		<LinkButton label="More" icon="add" on:click={() => ($menuOpen = true)} />
	</div>
	<h2 class="center">Latest Updates</h2>
	<div clas="columnCentered">
		{#each posts as post, i}
			<Post data={post} index={i} />
		{/each}
	</div>
</Layout>
