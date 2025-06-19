<script>
	import { page } from '$app/state';
	import Layout from 'components/Layout.svelte';
	import LinkButton from 'components/LinkButton.svelte';

	console.log(page.error);
</script>

<Layout title="Error">
	{#if page?.status == 404}
		<h1>404: Not found</h1>
		<p>You just hit a route that doesn't exist... the sadness.</p>
		<p>If you weren't expecting this to happen, <a href="/feedback">send us a message</a>.</p>
	{:else}
		<h1>{page?.error?.name} {page?.error?.message}</h1>
		{#if page?.error?.stack}
			<pre style="overflow-x: auto; opacity: 0.75;">{page?.error?.stack}</pre>
		{/if}
		<LinkButton onclick={() => window.location.reload()} label="Try again" icon="refresh" />
		<p>If this keeps happening, <a href="/feedback">send us a message</a>.</p>
	{/if}
</Layout>
