<script>
	/** @type {{ key: string; enabled: boolean; name: string }[]} */
	export let tabs;

	let actualTabs = tabs.filter((tab) => tab.enabled ?? true);
	let selectedTab = 0;
</script>

{#if actualTabs.length > 0}
	<div class="container">
		{#each tabs as { name: tab }, i}
			<button class="tab" class:selected={i === selectedTab} on:click={() => (selectedTab = i)}>
				{tab}
			</button>
		{/each}
	</div>
	<slot key={tabs[selectedTab]?.key} />
{/if}

<style lang="scss">
	.container {
		display: flex;
		align-items: stretch;
		justify-content: stretch;
		box-sizing: border-box;
		// border: 1px solid var(--text-translucent);
		background: var(--text-translucent);
		border-top-left-radius: 8px;
		border-top-right-radius: 8px;
		width: 100%;
		// overflow: hidden;
	}

	.tab {
		all: unset;
		flex: 1;
		font-size: 0.9em;
		font-weight: bold;
		text-transform: uppercase;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 8px;
		transition: 120ms ease;
		border-bottom: 4px solid transparent;
		color: var(--text-translucent-2);
		cursor: pointer;
	}

	.selected {
		color: var(--text);
		border-bottom-color: currentColor;
	}
</style>
