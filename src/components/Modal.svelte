<script>
	import LinkButton from './LinkButton.svelte';
	import { createEventDispatcher, onMount, tick } from 'svelte';
	const dispatch = createEventDispatcher();

	export let show = false;
	export let danger = false; // when you're deleting something
	export let confirmation = true; // false only shows the close button
	export let closeText = null;
	export let confirmText = null;

	/** @type {HTMLDialogElement} */
	let dialog;

	$: if (dialog) {
		if (show) dialog.showModal();
		else dialog.close();
	}

	onMount(async () => {
		// polyfill for some slightly older safari versions that we still kinda need to support
		if (!window.HTMLDialogElement) {
			try {
				await tick(); // wait for dialog to be in DOM
				const dialogPolyfill = (await import('dialog-polyfill')).default;
				console.log(dialog);
				dialogPolyfill.registerDialog(dialog);
				await import('dialog-polyfill/dist/dialog-polyfill.css');
			} catch (e) {
				console.error('dialog polyfill error', e);
			}
		}
	});
</script>

<!-- svelte-ignore a11y-click-events-have-key-events a11y-no-noninteractive-element-interactions -->
<dialog
	bind:this={dialog}
	on:close={() => {
		if (dialog.returnValue === 'confirm') dispatch('confirm'); // when explicitly confirming
		else dispatch('cancel'); // for any other reason (click out, etc.)
		show = false;
		dispatch('close', dialog.returnValue); // always (for resetting content or handling a custom return), DONE LAST
		dialog.returnValue = '';
	}}
	on:click|self={() => dialog.close()}
>
	<form method="dialog">
		<div class="content">
			<slot />
		</div>
		<div class="horizPanel" style="justify-content: flex-end;">
			<LinkButton
				icon="close"
				label={closeText || (confirmation ? 'Cancel' : 'Close')}
				props={{ autofocus: '', type: 'submit', formnovalidate: '' }}
			/>
			{#if confirmation}
				<LinkButton
					icon={danger ? 'delete' : 'check'}
					label={confirmText || 'Confirm'}
					props={{ type: 'submit', value: 'confirm' }}
					{danger}
					active={!danger}
				/>
			{/if}
			<slot name="buttons" />
		</div>
	</form>
</dialog>

<style lang="scss">
	// https://github.com/whatwg/html/issues/7732
	// dialog {
	// 	overscroll-behavior-y: contain;
	// 	overflow: auto;
	// }

	// native
	dialog::backdrop,
	// pollyfill
	dialog :global(+ .backdrop) {
		background-color: rgba(0, 0, 0, 0.4);
		animation: fade 250ms ease;
	}

	dialog[open] {
		border: none;
		padding: 0;

		width: calc(100% - 16px);
		max-width: 40rem;

		border-radius: 8px;
		background-color: var(--light);
		box-shadow: var(--button-shadow);
		font-size: 17px;

		form {
			width: 100%;
			min-height: 15vh;
			box-sizing: border-box;
			padding: 12px; // so clicking on the edges won't count as clicking outside

			display: flex;
			flex-direction: column;
			align-items: center;
			justify-content: space-between;
			gap: 0.5em;

			> :global(*) {
				width: 100%;
			}
			.content {
				> :global(*) {
					&:first-child {
						margin-top: 0;
					}
					margin-block: 0.5em;
				}
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
