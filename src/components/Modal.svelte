<script lang="ts">
	import { onMount, tick, type Snippet } from 'svelte';
	import LinkButton from './LinkButton.svelte';

	/** @type {Props} */
	let {
		show = $bindable(false),
		danger = false,
		confirmation = true,
		closeText = undefined,
		confirmText = 'Confirm',
		children,
		buttons,
		onconfirm,
		oncancel,
		onclose,
	}: {
		show?: boolean;
		/** when you're deleting something */
		danger?: boolean;
		/** false only shows the close button */
		confirmation?: boolean;
		closeText?: string | undefined;
		confirmText?: string | undefined;

		children?: Snippet;
		buttons?: Snippet;

		onconfirm?: (prevent: () => void) => void;
		oncancel?: (prevent: () => void) => void;
		onclose?: (returnValue: string) => void;
	} = $props();

	let dialog: HTMLDialogElement;

	$effect(() => {
		if (dialog) {
			if (show) dialog.showModal();
			else dialog.close();
		}
	});

	export const showModal = () => {
		show = true;
	};

	export const close = () => {
		show = false;
	};

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

<!-- svelte-ignore a11y_click_events_have_key_events, a11y_no_noninteractive_element_interactions -->
<dialog
	bind:this={dialog}
	onclose={() => {
		let prevented = false;
		const prevent = () => {
			dialog.showModal();
			prevented = true;
		};

		if (dialog.returnValue === 'confirm')
			onconfirm?.(prevent); // when explicitly confirming
		else oncancel?.(prevent); // for any other reason (click out, etc.)
		if (!prevented) {
			console.log('close');
			show = false;
			onclose?.(dialog.returnValue); // always (for resetting content or handling a custom return), DONE LAST
		}
		dialog.returnValue = '';
	}}
	onclick={(e) => {
		if (e.target === dialog) dialog.close();
	}}
>
	<form method="dialog">
		<div class="content">
			{@render children?.()}
		</div>
		<div class="horizPanel" style="justify-content: flex-end;">
			<LinkButton
				icon="close"
				label={closeText || (confirmation ? 'Cancel' : 'Close')}
				autofocus={true}
				type="submit"
				formnovalidate={true}
			/>
			{#if confirmation}
				<LinkButton
					icon={danger ? 'delete' : 'check'}
					label={confirmText}
					active={!danger || 'danger'}
					type="submit"
					value="confirm"
				/>
			{/if}
			{@render buttons?.()}
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
		background-color: rgba(0, 0, 0, 0.5);
		// fixme: show animation only when dialog isn't already open
		// animation: fade 250ms ease;
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
					margin-block: 0.5em;
					&:first-child {
						margin-top: 0;
					}
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
