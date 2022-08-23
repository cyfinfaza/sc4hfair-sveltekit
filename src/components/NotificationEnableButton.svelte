<script>
	import LinkButton from 'components/LinkButton.svelte';
	import { checkNotificationStatus, subscribe, unsubscribe } from 'logic/webpush';
	import { onMount } from 'svelte';
	import { isOnline } from 'logic/stores.js';
	let loading = 'Loading notification status...';
	let notificationStatus = false;
	let subscriptionError = null;

	async function checkSubscription() {
		try {
			notificationStatus = await checkNotificationStatus();
			loading = null;
		} catch (e) {
			subscriptionError = e;
			loading = 'Notifications unavailable';
		}
	}

	$: {
		if ($isOnline) {
			checkSubscription();
		}
	}
</script>

<div class="notificationEnableButton">
	<LinkButton
		label={(!$isOnline && 'Notifications unavailable offline') ||
			loading ||
			(notificationStatus
				? 'Notifications enabled (tap to disable)'
				: 'Notifications disabled (tap to enable)')}
		icon={notificationStatus ? 'notifications' : 'notifications_off'}
		disabled={loading !== null || !$isOnline}
		active={notificationStatus}
		on:click={async () => {
			if (loading !== null) return;
			try {
				subscriptionError = null;
				if (!notificationStatus) {
					loading = 'Enabling notifications...';
					await subscribe();
				} else {
					loading = 'Disabling notifications...';
					await unsubscribe();
				}
				notificationStatus = !notificationStatus;
			} catch (e) {
				subscriptionError = e;
			}
			loading = null;
			await checkSubscription();
		}}
	/>
	{#if subscriptionError}
		<p style="color: red; font-size: 0.9rem;">
			{subscriptionError}
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
