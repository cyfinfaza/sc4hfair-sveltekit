<script>
	import AppLogo from 'assets/favicon.svg?component';
	import LinkButton from 'components/LinkButton.svelte';
</script>

<div class="container">
	<AppLogo />

	<div>
		<h1>Offline</h1>
		<p>This page is not available offline. Please try again when you have a connection.</p>
	</div>

	<div class="horizPanel">
		<LinkButton on:click={() => window.location.reload()} label="Try again" icon="refresh" />
		<LinkButton on:click={() => (window.location.href = '/')} label="Go home" icon="home" />
	</div>
</div>

<style>
	.container {
		height: 100vh;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: 16px;
		text-align: center;
	}
	* {
		margin: 0;
	}
	:global(svg) {
		max-width: 100px;
		fill: currentColor;
	}
</style>
