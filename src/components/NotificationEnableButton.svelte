<script>
	import LinkButton from 'components/LinkButton.svelte';
	import { isOnline } from 'logic/stores.js';
	import { notificationStatus, subscribe, unsubscribe } from 'logic/webpush.js';

	// initial state
	/**
	 * overrides button text, used while an operation (like fetch) is happening
	 *
	 * @type {string | null}
	 */
	let loading = 'Loading notification status…';

	$: if ($notificationStatus.ready !== false) loading = null;
</script>

<div class="notificationEnableButton">
	<LinkButton
		label={(!$isOnline && 'Notifications unavailable offline') ||
			loading ||
			($notificationStatus?.available ?
				$notificationStatus?.registered ?
					'Notifications enabled (tap to disable)'
				:	'Notifications disabled (tap to enable)'
			:	'Notifications unavailable')}
		icon={$notificationStatus?.available && $notificationStatus?.registered ?
			'notifications'
		:	'notifications_off'}
		disabled={loading !== null || !$notificationStatus?.available || !$isOnline}
		active={$notificationStatus?.available && $notificationStatus?.registered}
		on:click={async () => {
			if (loading !== null || !$notificationStatus?.available) return;
			try {
				// await updateNotificationStatus();
				let data;
				console.log($notificationStatus);
				if (!$notificationStatus?.registered) {
					loading = 'Enabling notifications…';
					data = await subscribe();
				} else {
					loading = 'Disabling notifications…';
					data = await unsubscribe();
				}
				notificationStatus.update((oldStatus) => ({
					available: oldStatus.available,
					registered: data.registered,
					message: data.message,
				}));
			} catch (/** @type{any}*/ e) {
				notificationStatus.update((oldStatus) => ({ ...oldStatus, message: e?.message })); // we failed, revert with message
			}
			loading = null;
		}}
	/>
	{#if $notificationStatus?.message}
		<p style="color: red; font-size: 0.9rem;">
			{$notificationStatus.message}
		</p>
	{/if}
</div>

<style lang="scss">
	.notificationEnableButton {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		gap: 8px;
		> * {
			margin: 0;
		}
	}
</style>
