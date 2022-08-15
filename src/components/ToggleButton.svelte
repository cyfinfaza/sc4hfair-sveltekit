<script>
	export let value = false;
</script>

<button class="theButton" class:on={value} on:click={(_) => (value = !value)}>
	<slot />
</button>

<style>
	.theButton {
		transition: background-color 120ms ease;
	}
	.on {
		background-color: var(--green);
		color: var(--green-text);
	}
</style>
