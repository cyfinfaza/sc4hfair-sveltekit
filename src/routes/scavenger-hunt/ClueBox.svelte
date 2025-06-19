<script lang="ts">
	import LinkButton from 'components/LinkButton.svelte';
	import { getContext } from 'svelte';
	import type { Context } from './+page.svelte';
	const { atIndex, hintsUsed, addHintUsed, clues, startScanning, destination } =
		getContext<Context>('sh');

	let {
		index = $bindable(),
		winner = false,
	}: {
		index: number;
		winner?: boolean;
	} = $props();
	if (winner) index = clues.length;
</script>

<div class:disabled={index > $atIndex} class:winner class="card">
	<h2 class="clueIndexLabel">
		{#if winner}
			<span class="material-icons">star</span>
		{:else}
			{index + 1}
		{/if}
	</h2>
	{#if index <= $atIndex}
		<div class="clue">
			{#if winner}
				<p>
					You've finished the scavenger hunt {$hintsUsed.length ?
						`with ${$hintsUsed.length === 1 ? 'only 1 hint' : `${$hintsUsed.length} hints`}`
					:	'without any hints'}! Go back to the {destination} to claim your prize!
				</p>
			{:else}
				<p>{clues[index].clue}</p>
				{#if clues[index].hint && $hintsUsed.includes(clues[index].code)}
					<p><strong>Hint:</strong> {clues[index].hint}</p>
				{/if}
				{#if index < $atIndex}
					<span class="material-icons checkIcon">check</span>
				{:else if clues[index].code}
					<div class="horizPanel">
						{#if clues[index].hint && !$hintsUsed.includes(clues[index].code)}
							<LinkButton
								label="Hint"
								onclick={() => addHintUsed(clues[index].code)}
								icon="emoji_objects"
							/>
						{/if}
						<LinkButton label="Scan" onclick={() => startScanning()} icon="qr_code_scanner" />
					</div>
				{/if}
			{/if}
		</div>
	{:else}
		<span class="material-icons">lock</span>
	{/if}
</div>

<style>
	.card {
		background: var(--light);
		border-radius: 8px;
		padding: 16px;
		display: flex;
		gap: 16px;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 16px;
	}
	.card * {
		margin: 0;
	}
	.disabled {
		/* background-color: var(--grey);
		color: var(--grey-text); */
		filter: contrast(0.7);
		min-height: 78px;
		box-sizing: border-box;
	}
	.winner {
		background: var(--yellow);
		color: var(--yellow-text);
		font-weight: bold;
	}
	.clueIndexLabel {
		font-size: 2em;
		font-weight: bold;
	}
	.winner .clueIndexLabel span {
		display: flex;
		align-items: center;
		font-size: 1em;
	}
	.clue {
		display: flex;
		flex-direction: column;
		align-items: flex-end;
		text-align: right;
		gap: 8px;
	}
	.checkIcon {
		padding: 4px;
		border-radius: 50%;
		background-color: var(--green);
		color: var(--green-text);
	}
</style>
