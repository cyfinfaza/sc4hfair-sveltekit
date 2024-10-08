<script>
	import { browser } from '$app/environment';
	import Layout from 'components/Layout.svelte';
	import Modal from 'components/Modal.svelte';
	import NotificationEnableButton from 'components/NotificationEnableButton.svelte';
	import ToggleButton from 'components/ToggleButton.svelte';
	import tentSlugs from 'data/tentSlugs.json';
	import { eventIsFuture, MINUTES_BEFORE_NOTIFICATION } from 'logic/scheduling.js';
	import { exactSearch } from 'logic/search.js';
	import { kioskMode } from 'logic/stores.js';
	import { getSubscription, notificationStatus } from 'logic/webpush.js';
	import EventBox from './EventBox.svelte';

	/** @type {import('./$types').PageData} */
	export let data;

	/** @type {string[]} */
	let subscribedEvents = [];

	/** @type {Modal} */
	let subscribeModal;
	/** @type {() => Promise<void>} */
	let toggleNotificationEnabledClick;

	const loadScheduledNotifications = async () => {
		const sub = await getSubscription();
		const res = await fetch(
			`/api/webpush/scheduledNotifications?subscription=${encodeURIComponent(JSON.stringify(sub))}`
		);

		if (!res.ok) {
			console.error('failed to load scheduled notifications:', res);
			subscribedEvents = [];
			return;
		}

		/**
		 * @type {{
		 * 	type: 'success' | 'error';
		 * 	message: string?;
		 * 	subscriptionId: string;
		 * 	eventIds: string[];
		 * }}
		 */
		const data = await res.json();
		if (data.type === 'error') {
			console.error('error loading scheduled notifications:', data);
			subscribedEvents = [];
			return;
		}

		subscribedEvents = data.eventIds;

		let currentSubscriptionId = localStorage.getItem('subscriptionId');
		if (currentSubscriptionId && currentSubscriptionId !== data.subscriptionId) {
			console.warn('subscription id changed', currentSubscriptionId, data.subscriptionId);
			// this should never happen as subscription id persists changing sub_info
		}
		notificationStatus.update((oldStatus) => ({
			...oldStatus,
			subscriptionId: data.subscriptionId, // populate this in
		}));
		localStorage.setItem('subscriptionId', data.subscriptionId);

		if (pendingEventSubscription) {
			setEventSubscription(...pendingEventSubscription);
			pendingEventSubscription = null;
		}
	};

	/** @type {boolean | undefined} */
	let lastRegistered = undefined;
	$: {
		// only update on registration change
		if ($notificationStatus.registered !== lastRegistered) {
			// $notificationStatus also will retrigger on online
			if (browser && $notificationStatus.registered) {
				loadScheduledNotifications();
				subscribeModal?.close();
			} else subscribedEvents = [];
			lastRegistered = $notificationStatus.registered;
		}
	}

	/** @type {[string, boolean]?} */
	let pendingEventSubscription = null;

	/**
	 * @param {string} eventId
	 * @param {boolean} subscribed
	 */
	const setEventSubscription = async (eventId, subscribed) => {
		if ($notificationStatus.registered === false) {
			pendingEventSubscription = [eventId, subscribed];
			subscribeModal.showModal();
			return;
		}
		const event = data.events.find((event) => event.sys.id === eventId);
		if (subscribedEvents === undefined || event === undefined) return;

		let oldSubscribedEvents = [...subscribedEvents];
		let method, body;
		if (subscribed) {
			subscribedEvents = [...subscribedEvents, eventId];
			method = 'POST';
			body = {
				eventId,
				when: new Date(
					new Date(event.time).getTime() - MINUTES_BEFORE_NOTIFICATION * 60e3
				).toISOString(),
			};
		} else {
			subscribedEvents = subscribedEvents.filter((id) => id !== eventId);
			method = 'DELETE';
			body = { eventId };
		}
		console.log('subscribedEvents', subscribedEvents);
		const res = await fetch('/api/webpush/scheduledNotifications', {
			method,
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ subscription: await getSubscription(), ...body }),
		});
		if (!res.ok) {
			console.error('error setting event subscription:', res);
			subscribedEvents = oldSubscribedEvents;
		} else if ((await res.json()).type === 'error') {
			console.error('failed to set event subscription:', res);
			subscribedEvents = oldSubscribedEvents;
		}
	};

	let selectedTent = 'All';
	let showingPast = false;
	let searchQuery = '';
	let showingOnlySubscribedEvents = false;

	let results = [];
	$: results = exactSearch(
		searchQuery,
		data.events.filter(
			(element) =>
				((selectedTent === 'All' || selectedTent === element.tent) &&
					(eventIsFuture(element) || showingPast)) ||
				(browser && window.location?.hash === '#' + element.sys.id)
		),
		'title',
		['tentName']
	).filter((element) => !showingOnlySubscribedEvents || subscribedEvents?.includes(element.sys.id));
</script>

<Layout title="Schedule">
	<h1 class="center">Events</h1>
	<div class="filterOptions">
		<p>Filter:</p>
		<select bind:value={selectedTent} name="Tent">
			{#each data.eventTentsList as tent (tent)}
				<option value={tent}>
					{(tent !== 'All' && tentSlugs[tent]) || tent}
				</option>
			{/each}
		</select>
		<input type="text" placeholder="Search" bind:value={searchQuery} />
		<ToggleButton bind:value={showingPast}>Show Past Events</ToggleButton>
		{#if !$kioskMode}
			<ToggleButton bind:value={showingOnlySubscribedEvents}
				>Show Only Subscribed Events</ToggleButton
			>
		{/if}
	</div>
	{#if !$kioskMode}
		<p class="center">
			Click the bell icon to receive a notification {MINUTES_BEFORE_NOTIFICATION}
			minutes before the event starts. Manage your subcription in the
			<a href="/settings#notifications">settings</a>.
		</p>
	{/if}
	<div class="columnCentered">
		{#each results as event, i (event.sys.id)}
			<EventBox
				{event}
				index={i}
				subscribed={subscribedEvents.includes(event.sys.id)}
				{setEventSubscription}
			/>
		{/each}
	</div>
</Layout>

<Modal
	show={false}
	bind:this={subscribeModal}
	confirmation
	on:confirm={({ detail }) => {
		if (!$notificationStatus.registered) {
			detail.cancel();
			toggleNotificationEnabledClick().then(() => {
				if ($notificationStatus.registered) subscribeModal.close();
			});
		}
	}}
>
	<h2>Subscribe to notifications</h2>
	<p>
		First subscribe to app notifications to receive a reminder {MINUTES_BEFORE_NOTIFICATION} minutes
		before the event starts.
	</p>
	<p>You will also receive fair news and emergency alerts.</p>
	<NotificationEnableButton bind:onClick={toggleNotificationEnabledClick} />
</Modal>

<style>
	.filterOptions {
		width: 100%;
		display: flex;
		justify-content: center;
		margin-bottom: 16px;
		align-items: center;
		gap: 8px;
		flex-wrap: wrap;
	}
	.filterOptions > * {
		margin-block: 0;
	}
</style>
