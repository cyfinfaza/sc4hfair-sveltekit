<script>
	import { createEventDispatcher } from 'svelte';
	const dispatch = createEventDispatcher();
	import LinkButton from './LinkButton.svelte';
	import { onMount } from 'svelte';

	export let show = false;
	export let danger = true; // when you're deleting something

	/** @type {HTMLDialogElement} */
	let dialog;

	onMount(() => {
		dialog.addEventListener('close', () => {
			if (dialog.returnValue === 'confirm') dispatch('confirm'); // when explicitly confirming
			else dispatch('cancel'); // for any other reason (click out, etc.)
			show = false;
			dispatch('close'); // always (for resetting content), DONE LAST
		});
		dialog.addEventListener('click', (e) => {
			if (e.target.nodeName === 'DIALOG') {
				dialog.close(); // close when clicking outside
			}
		});
	});

	$: if (dialog) {
		if (show) dialog.showModal();
		else dialog.close();
	}
</script>

<dialog bind:this={dialog}>
	<form method="dialog">
		<slot />
		<div class="horizPanel">
			<LinkButton
				icon="close"
				label="Cancel"
				props={{ autofocus: '', type: 'submit', formnovalidate: '' }}
			/>
			<LinkButton
				icon={danger ? 'delete' : 'check'}
				label="Confirm"
				props={{ type: 'submit', value: 'confirm' }}
				{danger}
				active={!danger}
			/>
		</div>
	</form>
</dialog>

<style lang="scss">
	// https://github.com/whatwg/html/issues/7732
	// dialog {
	// 	overscroll-behavior-y: contain;
	// 	overflow: auto;
	// }

	dialog::backdrop {
		background-color: rgba(0, 0, 0, 0.4);
		animation: fade 250ms ease;
	}

	dialog[open] {
		border: none;
		padding: 0;

		border-radius: 8px;
		background-color: var(--light);
		box-shadow: var(--button-shadow);
		font-size: 17px;

		form {
			width: clamp(260px, 50vw, 40rem);
			min-height: 15vh;
			box-sizing: border-box;
			padding: 12px; // so clicking on the edges won't count as clicking outside

			display: flex;
			flex-direction: column;
			align-items: center;
			justify-content: center;

			> :global(*) {
				margin: 0.5em 0;
				width: 100%;
			}
		}
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
