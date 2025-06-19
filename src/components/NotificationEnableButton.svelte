<script lang="ts">
	import LinkButton from 'components/LinkButton.svelte';
	import { isOnline } from 'logic/stores.svelte';
	import { notificationStatus, subscribe, unsubscribe } from 'logic/webpush';

	// initial state
	/** overrides button text, used while an operation (like fetch) is happening */
	let loading: string | null = $state('Loading notification status…');

	$effect(() => {
		if ($notificationStatus.ready !== false) loading = null;
	});

	let active = $derived($notificationStatus?.available && $notificationStatus?.registered);

	export const onclick = async () => {
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
				subscriptionId: data.subscriptionId,
			}));
		} catch (e: any) {
			notificationStatus.update((oldStatus) => ({ ...oldStatus, message: e?.message })); // we failed, revert with message
		}
		loading = null;
	};
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
		icon={active ? 'notifications' : 'notifications_off'}
		disabled={loading !== null || !$notificationStatus?.available || !$isOnline}
		active={active || 'warning'}
		{onclick}
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
