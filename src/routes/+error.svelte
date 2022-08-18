<script>
	import { page } from '$app/stores';
	import Layout from 'components/Layout.svelte';

	console.log(error);
</script>

<Layout title="Error">
	{#if $page.status == 404}
		<h1>404: Not found</h1>
		<p>You just hit a route that doesn't exist... the sadness.</p>
	{:else}
		<h1>{$page.error.name}</h1>
		<pre style="overflow-x: auto; opacity: 0.75;">{$page.error.stack.replace(/ {4}/g, '\t')}</pre>
	{/if}
	<p>If you weren't expecting this to happen, <a href="/feedback">send us a message</a>.</p>
</Layout>
