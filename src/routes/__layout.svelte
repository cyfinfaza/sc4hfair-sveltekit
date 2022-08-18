<script context="module">
	import { getSponsors } from 'logic/contentful.js';
	export async function load({ fetch }) {
		const resp = await getSponsors(fetch);
		return { props: { sponsors: resp } };
	}
</script>

<script>
	import 'styles/global.css';
	import 'styles/material-icons.css';
	import 'styles/fonts.css';
	import { setContext } from 'svelte';
	export let sponsors;
	setContext('sponsors', sponsors);
</script>

<slot />
