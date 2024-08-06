<script>
	export let value = false;
</script>

<button class:on={value} on:click={() => (value = !value)}>
	<slot />
</button>

<style>
	button {
		transition: background-color 120ms ease;
	}
	.on {
		background-color: var(--green);
		color: var(--green-text);
	}
</style>
