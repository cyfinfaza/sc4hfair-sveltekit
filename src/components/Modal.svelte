<script>
	import { createEventDispatcher } from 'svelte';
	const dispatch = createEventDispatcher();
	import LinkButton from './LinkButton.svelte';

	export let show;
	export let confirmation = false; // show confirm/cancel buttons instad of just close
	export let danger = true; // when you're deleting something

	const close = (e, confirmed = false) => {
		console.log(e);
		// only close if its not actually the modal
		if (
			e === null ||
			e.target.classList.contains('wrapper') ||
			e.target.classList.contains('close')
		) {
			if (confirmed) dispatch('confirm'); // when confirming
			else dispatch('close'); // when cancelling
			show = false;
			console.trace('closing modal');
		}
	};
</script>

{#if show}
	<div class="wrapper" on:click={close} role="dialog">
		<div class="content">
			{#if !confirmation}
				<i
					class="material-icons close"
					on:click={() => close(null, false)}
					role="button"
					aria-label="Close"
					tabIndex={0}>close</i
				>
			{/if}
			<slot />
			{#if confirmation}
				<div class="horizPanel" style:margin-op=".75em">
					<LinkButton icon="close" label="Cancel" on:click={() => close(null, false)} />
					<LinkButton
						icon={danger ? 'delete' : 'check'}
						label="Confirm"
						on:click={() => close(null, true)}
						{danger}
					/>
				</div>
			{/if}
		</div>
	</div>
{/if}

<style>
	.wrapper {
		position: fixed;
		z-index: 999;
		left: 0;
		top: 0;
		width: 100%;
		height: 100%;
		overflow: auto;
		background-color: rgba(0, 0, 0, 0.4);

		display: flex;
		align-items: center;

		animation: fade 250ms ease;
	}

	.content {
		margin: 0 auto;
		width: clamp(330px, 50vw, 40rem);
		min-height: 30vh;
		border-radius: 8px;
		background-color: var(--light);
		box-shadow: var(--button-shadow);
		padding: 12px;
		box-sizing: border-box;
		font-size: 17px;
		position: relative;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}

	.content > :global(*) {
		margin: 4px 0;
		width: 100%;
	}

	.close {
		position: absolute;
		top: 8px;
		right: 8px;
		opacity: 0.3;
	}

	@keyframes fade {
		from {
			opacity: 0;
		}
		to {
			opacity: 1;
		}
	}
</style>
