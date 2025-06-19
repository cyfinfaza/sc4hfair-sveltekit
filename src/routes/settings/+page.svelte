<script lang="ts">
	import { browser, dev, version } from '$app/environment';
	import { goto } from '$app/navigation';
	import InstallInstructions from 'components/InstallInstructions.svelte';
	import KioskPitch from 'components/KioskPitch.svelte';
	import LabeledInput from 'components/LabeledInput.svelte';
	import Layout from 'components/Layout.svelte';
	import LinkButton from 'components/LinkButton.svelte';
	import Modal from 'components/Modal.svelte';
	import NoOffline from 'components/NoOffline.svelte';
	import NotificationEnableButton from 'components/NotificationEnableButton.svelte';
	import SignInButtons from 'components/SignInButtons.svelte';
	import { logout, session } from 'logic/auth';
	import { BRANCH, BUILD_LOCATION, BUILD_TIME } from 'logic/constants';
	import { interestsSlugs } from 'logic/interests';
	import { isStandalone } from 'logic/platform';
	import { isOnline, kioskMenuSize, kioskMode } from 'logic/stores.svelte';
	import { getSubscription, notificationStatus, subscribe, unsubscribe } from 'logic/webpush';
	import { untrack } from 'svelte';
	import { writable, type Writable } from 'svelte/store';

	type Form = Partial<{
		name: string;
		preferred_email: string;
		phone: string;
		graduation: number | null;
	}>;

	const form: Writable<Form> = writable({
		name: '',
		preferred_email: '',
		phone: '',
		graduation: null,
	});
	let cloudForm: Form = $state({});

	let isInfoFormDisabled = $derived.by(() => {
		if (!$form || !cloudForm) return true;
		// only check certain properties
		return (['name', 'preferred_email', 'phone', 'graduation'] as const).every(
			(key) => $form[key] === cloudForm[key]
		);
	});

	let confirmReset: 'sh' | 'interests' | null = $state(null); // modal for confirmation

	let showingAdditionalBuildInfo = $state(dev),
		showDebugModal = $state(false),
		showKioskSizeAdjuster = $state(false);

	function toggleFullscreen() {
		if (!document.fullscreenElement && !(document as any).webkitFullscreenElement) {
			if (document.documentElement.requestFullscreen) document.documentElement.requestFullscreen();
			else (document.documentElement as any).webkitRequestFullscreen();
		} else {
			if (document.exitFullscreen) document.exitFullscreen();
			else (document as any).webkitExitFullscreen();
		}
	}

	$effect(() => {
		(async () => {
			if ($session) {
				const { profile } = await (
					await fetch('/api/profile', {
						credentials: 'include',
					})
				).json();
				cloudForm = profile;
				$form = { ...untrack(() => cloudForm) };
			}
		})();
	});
</script>

<Layout title="Settings">
	{#if $kioskMode}
		<h1>Enjoying the app?</h1>
		<KioskPitch box={false} />
	{:else}
		<h1>Account</h1>
		{#if $session}
			<p>You are signed in as <strong>{$session?.email}</strong></p>
			<p>
				<LinkButton label="Sign out" icon="logout" onclick={() => logout()} />
			</p>
			<h2>
				Additional information <small>(optional)</small>
			</h2>
			<table style="width: 100%; margin: 1rem 0;">
				<tbody>
					<LabeledInput {form} name="name" label="Full name" />
					<LabeledInput {form} name="preferred_email" label="Preferred email" type="email" />
					<LabeledInput {form} name="phone" label="Phone number" type="tel" />
					<LabeledInput
						{form}
						name="graduation"
						label="Graduation year"
						type="number"
						min="1900"
						max="2099"
						step="1"
					/>
				</tbody>
			</table>
			<LinkButton
				label="Save"
				icon="save"
				onclick={async () => {
					const res = await fetch('/api/profile', {
						method: 'PATCH',
						headers: { 'Content-Type': 'application/json' },
						credentials: 'include',
						body: JSON.stringify($form),
					});
					if (res.ok) {
						const { profile } = await res.json();
						cloudForm = { ...profile };
					} else {
						const error = await res.json();
						alert(error.message || 'Failed to save profile');
					}
				}}
				disabled={isInfoFormDisabled || !$isOnline}
				alert={!isInfoFormDisabled}
			/>
		{:else if !$isOnline}
			<NoOffline />
		{:else}
			<SignInButtons redirect="/settings" />
		{/if}

		<h1>Add to homescreen</h1>
		{#if $isStandalone}
			<p>This site is already running in standalone mode.</p>
		{:else}
			<p>To add the fair app to your homescreen:</p>
			<InstallInstructions />
		{/if}

		<h1 id="notifications">Notifications</h1>
		<NotificationEnableButton />

		<h1>Clear data</h1>
		<p class="horizPanel2">
			<LinkButton
				label="Reset Scavenger Hunt"
				onclick={() => (confirmReset = 'sh')}
				icon="restart_alt"
			/>
			{#if $session}
				<LinkButton
					label="Clear Interest List"
					onclick={() => (confirmReset = 'interests')}
					icon="clear_all"
				/>
			{/if}
		</p>
		<Modal
			show={!!confirmReset}
			danger
			onclose={() => (confirmReset = null)}
			onconfirm={async () => {
				switch (confirmReset) {
					case 'sh':
						for (let i = 0; i < localStorage.length; i++) {
							const key = localStorage.key(i);
							if (key?.startsWith('sh_')) localStorage.removeItem(key);
						}
						goto('/scavenger-hunt');
						break;
					case 'interests':
						localStorage.removeItem('cim_intent');

						const res = await fetch('/api/interests', {
							method: 'DELETE',
							credentials: 'include',
						});

						if (res.ok) {
							console.log('Cleared interests');
							interestsSlugs.set([]);
						} else {
							alert('Failed to clear interests');
						}

						goto('/interests');
						break;
				}
			}}
		>
			<p>
				Are you sure you want to reset {confirmReset === 'sh' ?
					'your scavenger hunt progress'
				:	'this'}? You will not be able to restore it.
			</p>
			{#if confirmReset === 'sh'}
				<p>Note that you may only claim one prize per person.</p>
			{/if}
		</Modal>
	{/if}

	<h1>About</h1>
	<p>
		This app was created by the
		<a href="https://4hcomputers.club">Somerset County 4&#8209;H Computer Club</a>.
	</p>
	<p class="horizPanel2">
		<LinkButton label="Send feedback" disabled={!$isOnline} href="/feedback" icon="message" />
		<LinkButton label="Privacy Policy" href="/privacy-policy" icon="policy" />
	</p>
	<div style:opacity={0.5}>
		<!-- svelte-ignore a11y_no_noninteractive_element_to_interactive_role -->
		<code
			role="button"
			tabindex="0"
			onclick={() => (showingAdditionalBuildInfo = !showingAdditionalBuildInfo)}
			onkeydown={(e) =>
				e.key === 'Enter' && (showingAdditionalBuildInfo = !showingAdditionalBuildInfo)}
			style:cursor="pointer"
		>
			{version}
		</code>
		{#if showingAdditionalBuildInfo && browser}
			<br /><code>{BRANCH}</code>
			<br /><code>{BUILD_TIME}</code>
			<br /><code>{BUILD_LOCATION}</code>
			<div class="horizPanel2">
				<LinkButton icon="engineering" label="Debug" onclick={() => (showDebugModal = true)} />
				<LinkButton
					icon="settings_suggest"
					label="Unregister service worker"
					onclick={() => {
						navigator.serviceWorker.getRegistrations().then(function (registrations) {
							for (let registration of registrations) {
								registration.unregister();
							}
						});
					}}
				/>
				<LinkButton
					icon="update"
					label="Check for update (sw)"
					onclick={async () => {
						const swRegistration = await navigator.serviceWorker.getRegistration();
						swRegistration?.update();
					}}
				/>
				<LinkButton
					icon="cleaning_services"
					label="Remove localStorage item"
					onclick={() => {
						let key = prompt('Key:');
						if (key) localStorage.removeItem(key);
					}}
				/>
				<LinkButton
					icon="autorenew"
					label="Clear caches"
					onclick={() => {
						window.caches.keys().then(function (keys) {
							for (let key of keys) {
								window.caches.delete(key);
							}
						});
					}}
				/>
				<LinkButton
					icon="fullscreen"
					label="Toggle FS"
					onclick={() => {
						toggleFullscreen();
					}}
				/>
				{#if $kioskMode}
					<LinkButton icon="logout" label="Exit Kiosk" onclick={() => ($kioskMode = false)} />
					<LinkButton
						icon="expand_content"
						label="Kiosk Menu Size"
						onclick={() => (showKioskSizeAdjuster = true)}
					/>
				{:else}
					<LinkButton icon="tv" label="Enter Kiosk" onclick={() => ($kioskMode = true)} />
				{/if}
			</div>
			<hr />
			<div class="horizPanel2">
				<LinkButton
					icon="notifications_active"
					label="Test notification"
					onclick={async () => {
						new window.Notification('Fair Update', {
							body: 'The fair has been closed due to test weather.',
						});
					}}
				/>
				<LinkButton
					icon="notifications"
					label="Get notification subscription"
					onclick={async () => {
						console.log('getting subscription');
						const sub = await getSubscription();
						alert(JSON.stringify(sub));
						console.log(JSON.stringify(sub));
						console.log('got subscription');
					}}
				/>
				<LinkButton
					icon="notification_add"
					label="Subscribe to notifications"
					onclick={async () => {
						alert((await subscribe()).registered);
					}}
				/>
				<LinkButton
					icon="notifications_off"
					label="Unubscribe from notifications"
					onclick={async () => {
						alert(!(await unsubscribe()).registered);
					}}
				/>
			</div>
		{/if}
	</div>
</Layout>

<Modal bind:show={showDebugModal} confirmation={false}>
	{#if showDebugModal && typeof navigator !== 'undefined'}
		{#key showDebugModal}
			<table>
				<tbody>
					<tr>
						<td>UA</td>
						<td>{navigator.userAgent}</td>
					</tr>
					<tr>
						<td>SW</td>
						<td>
							{#await navigator.serviceWorker?.getRegistration()}
								...
							{:then reg}
								active: {reg?.active?.state}<br />
								waiting: {reg?.waiting?.state}<br />
								installing: {reg?.installing?.state}<br />
							{:catch error}
								{error.message}
							{/await}
						</td>
					</tr>
					<tr>
						<td>Notif</td>
						<td>
							permission: {Notification.permission}<br />
							subscriptionId: {$notificationStatus.subscriptionId}<br />
						</td>
					</tr>
					<tr>
						<td>Auth</td>
						<td>
							{#if $session}
								id: {$session.sub}<br />
								exp: {new Date($session.exp * 1000).toISOString()}<br />
							{:else}
								not signed in
							{/if}
						</td></tr
					>
					<tr>
						<td>Origin</td>
						<td>{location?.origin}</td>
					</tr>
				</tbody>
			</table>
		{/key}
	{/if}
</Modal>

<Modal bind:show={showKioskSizeAdjuster} confirmation={false}>
	<h2>Adjust Kiosk Menu Size</h2>
	<input
		type="range"
		min="10"
		max="90"
		style="width: 80%; display: block;"
		bind:value={$kioskMenuSize}
	/>
	<p>{$kioskMenuSize}</p>
</Modal>
