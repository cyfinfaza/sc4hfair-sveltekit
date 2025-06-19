<script lang="ts">
	let {
		value = $bindable(false),
		children,
	}: {
		value?: boolean;
		children: import('svelte').Snippet;
	} = $props();
</script>

<button class:on={value} onclick={() => (value = !value)}>
	{@render children()}
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
