<script>
	// If you look at the source code to cheat and get to the end, then congrats
	// I'm not going to try and do a fancy thing or whatever to prevent it
	// You win, come join the 4-H Computer Club

	import { browser } from '$app/environment';
	import KioskPitch from 'components/KioskPitch.svelte';
	import Layout from 'components/Layout.svelte';
	import LinkButton from 'components/LinkButton.svelte';
	import Modal from 'components/Modal.svelte';
	import * as _clueData from 'data/shClues.json';
	import { SCAVENGER_HUNT_CODE, SCAVENGER_HUNT_HINTS } from 'logic/constants';
	import { getPlatform, isStandalone } from 'logic/platform';
	import { pvtUpdate } from 'logic/pvt';
	import { kioskMode, pushPoprxUpdate } from 'logic/stores';
	import QrScanner from 'qr-scanner';
	import { onMount, setContext, tick } from 'svelte';
	import { writable } from 'svelte/store';
	import ClueBox from './ClueBox.svelte';
	import InstallInstructions from 'components/InstallInstructions.svelte';

	/** @typedef {{ code: string; clue: string; hint: string }} Clue */

	const clues = /** @type {Clue[]} */ (_clueData.clues);
	const falseCodes = /** @type {string[]} */ (_clueData.falseCodes);
	const year = _clueData.year;

	const currentYear = new Date().getFullYear();
	const enabled = clues.length && year === currentYear && !$kioskMode;

	/** @param {string | null} code */
	const getIndexFromCode = (code) => clues.findIndex((clue) => clue.code === code);
	/** @param {string | null} code */
	const getOffsetIndexFromCode = (code) => getIndexFromCode(code) + 1;

	let atIndex = writable(0);
	$: if ($atIndex > 0) localStorage.setItem(SCAVENGER_HUNT_CODE, clues[$atIndex - 1].code);

	let hintsUsed = writable([]);
	$: if ($hintsUsed.length) localStorage.setItem(SCAVENGER_HUNT_HINTS, JSON.stringify($hintsUsed));

	setContext('sh', {
		atIndex,
		hintsUsed,
		addHintUsed: (/** @type {string} */ code) => ($hintsUsed = [...$hintsUsed, code]),
		clues,
		finalInstructions: _clueData.finalInstructions,
		startScanning: () => (scanning = true),
	});

	/** @type {HTMLVideoElement} */
	let videoElement,
		/** @type {QrScanner | undefined} */
		qrScanner,
		compatible = false,
		scanning = false,
		scannerMessage = '';

	onMount(async () => {
		if (!browser || !enabled) return;

		let tmpIndex = getOffsetIndexFromCode(localStorage.getItem(SCAVENGER_HUNT_CODE));
		if (tmpIndex) $atIndex = tmpIndex;

		let hints = JSON.parse(localStorage.getItem(SCAVENGER_HUNT_HINTS) || '[]');
		if (hints && hints.length > 0) $hintsUsed = hints;

		try {
			checkCode(new URLSearchParams(window.location.search).get('code'), true); // Code from a scanned URL bringing them here
			// replaceState handled by +layout.svelte
		} catch (e) {
			console.error('error checking code from URL:', e);
		}
	});

	onMount(async () => {
		if (!enabled) return;

		try {
			compatible = typeof navigator === 'object' && (await QrScanner.hasCamera());
		} catch (_) {
			compatible = false;
		}
		console.log('camera compatible?', compatible);
		if (!compatible) return;

		try {
			qrScanner = new QrScanner(
				videoElement,
				({ data: code }) => {
					// Extract the code from a URL
					try {
						let tempCode = new URLSearchParams(new URL(code).search).get('code');
						if (typeof tempCode === 'string') code = tempCode;
					} catch (_) {
						// if it fails, it isn't a URL with a code
					}
					console.log('scanned', code);
					checkCode(code);
				},
				{
					preferredCamera: 'environment',
				}
			);
		} catch (e) {
			console.error(e);
			compatible = false;
		}

		() => qrScanner?.destroy();
	});

	onMount(() => {
		if (!browser || !enabled) return;
		let removeCallback = () => {};
		window.navigator.permissions
			.query({ name: /** @type {any} */ ('camera') })
			.then((permissionStatus) => {
				// let the library figure it out the first time
				const handleChange = () => {
					console.log(`camera permission state has changed to ${permissionStatus.state}`);
					compatible = permissionStatus.state === 'granted';
				};
				permissionStatus.addEventListener('change', handleChange);
				removeCallback = () => permissionStatus.removeEventListener('change', handleChange);
			});
		return () => removeCallback();
	});

	$: if (compatible && qrScanner) {
		if (scanning) {
			qrScanner.start().catch((e) => {
				console.error(e);
				compatible = false;
			});
		} else {
			scannerMessage = '';
			qrScanner.stop();
		}
	}

	/** @type {ReturnType<typeof setTimeout>} */
	let scannerMessageTimeout;

	/** @param {string | null} code */
	function checkCode(code, fromUrl = false) {
		let index = getIndexFromCode(code);
		console.table({ fromUrl, $atIndex });
		const clueIsInFalseList = code && falseCodes.includes(code);
		if (typeof code !== 'string' || !code) {
			console.log('doing nothing, code is not a string');
		} else if (index === -1) {
			if (fromUrl) scanning = true;
			if (clueIsInFalseList) scannerMessage = "This isn't the right code. Keep looking!\xa0😁";
			else scannerMessage = 'Invalid code. Make sure you are scanning scavenger hunt codes.\xa0🙃';
		} else if (index < $atIndex) {
			if (fromUrl) scanning = true;
			scannerMessage = "You've already scanned that code.";
		} else if (index > $atIndex) {
			if (fromUrl && $atIndex > 0) scanning = true;
			scannerMessage = "This isn't the right code. Keep looking!\xa0😁";
		} else {
			$atIndex = index + 1;
			scanning = false;
			scannerMessage = '';
			tick().then(() => {
				pvtUpdate();
				$pushPoprxUpdate?.();
			});
		}
		if (scannerMessageTimeout) clearTimeout(scannerMessageTimeout);
		scannerMessageTimeout = setTimeout(() => (scannerMessage = ''), 10000);
		if (!clues[$atIndex]) return;
		console.table({
			code,
			'index': index,
			'current code': clues[$atIndex].code,
			'current index': $atIndex,
			'current clue': clues[$atIndex].clue,
		});
	}

	let showEnterManuallyPrompt = false,
		manualCode = '';
</script>

<Layout title="Scavenger Hunt">
	{#if enabled}
		<div class="center">
			<h1>{year} Scavenger Hunt</h1>
			<p>
				Welcome to the 4‑H Fair Scavenger Hunt! Each clue will lead you to a <strong>QR code</strong
				>, which when scanned will unlock the next clue. The last clue will lead you to your prize!
			</p>
			<p style="margin-bottom: 0;">If you're stuck on a clue, try:</p>
			<div style="display: flex; justify-content: center;">
				<ul style="margin: 0; text-align: left; padding-inline-start: 1em;">
					<li>looking at the <a href="/map">fair map</a> or <a href="/clubs">clubs list</a></li>
					<li>talking to other 4‑Hers (they love to share)</li>
					<li>using a hint (they're free)</li>
					<li>searching for information in other resources</li>
				</ul>
			</div>
			<p>Hints used: {$hintsUsed.length}</p>
			{#each clues as _, index}
				<ClueBox {index} />
			{/each}
			<ClueBox index={clues.length} winner />
		</div>

		<p>
			You can reset the scavenger hunt in <a href="/settings">settings</a>, but only one prize may
			be claimed per group.
		</p>

		<!-- this div needs to always be rendered so the qr library doesn't die -->
		<div
			class="scanner"
			class:hidden={!scanning || !compatible}
			aria-hidden={!scanning || !compatible}
		>
			<div>
				<!-- svelte-ignore a11y-media-has-caption -->
				<video bind:this={videoElement} />
				<div class="scannerOverlay showSquare">
					<div class="scannerButtons">
						<LinkButton
							label="Enter manually"
							icon="keyboard"
							on:click={() => (showEnterManuallyPrompt = true)}
							acrylic
						/>
						<LinkButton label="Close" icon="close" on:click={() => (scanning = false)} acrylic />
					</div>
					<p class="scannerMessage">
						{scannerMessage ||
							"Try changing the angle to remove any glare. If the code won't scan, click the top left button to manually enter the code."}
					</p>
				</div>
			</div>
		</div>
		<!-- copy of scanner box for uncompatible devices -->
		<div
			class="scanner fallback"
			class:hidden={!scanning || compatible}
			aria-hidden={!scanning || compatible}
		>
			<div class="scannerOverlay">
				<LinkButton label="Close" icon="close" on:click={() => (scanning = false)} acrylic />
				<div class="scannerMessage">
					<p>{scannerMessage}</p>
					{#if getPlatform() === 'ios' && !$isStandalone}
						<p>To use the QR scanner, you may need to install this as an app.</p>
						<small>
							Note: Your progress might be reset. If you have already completed multiple clues,
							please see the 4-H Computers booth for assistance.
						</small>
						<InstallInstructions />
					{:else}
						<p>
							The scavenger hunt recommends a QR scanner. Check that your browser is allowing the
							app camera access to use the built-in one, or use an external scanner.
						</p>
					{/if}
					<LinkButton
						label="Retry permission"
						icon="flip_camera_ios"
						on:click={async () => {
							try {
								compatible = typeof navigator === 'object' && (await QrScanner.hasCamera());
								window.location.reload();
							} catch (_) {
								compatible = false;
							}
						}}
					/>
					<p>Alternatively, you can manually enter the code:</p>
					<LinkButton
						label="Enter manually"
						icon="keyboard"
						on:click={() => (showEnterManuallyPrompt = true)}
					/>
				</div>
			</div>
		</div>
	{:else}
		<div class="center">
			<h1>{currentYear} Scavenger Hunt</h1>
			{#if $kioskMode}
				<KioskPitch>
					<p>
						The scavenger hunt is not available at the kiosk. Please use a personal device to
						participate!
					</p>
					<p>Trust me, it's a lot of fun… and there's even a prize!</p>
				</KioskPitch>
			{:else}
				<p>The scavenger hunt is not ready yet, come back when the fair starts!</p>
			{/if}
		</div>
	{/if}
</Layout>

<Modal
	show={showEnterManuallyPrompt}
	on:close={() => {
		showEnterManuallyPrompt = false;
		manualCode = '';
	}}
	on:confirm={() => {
		checkCode(manualCode?.toLowerCase(), false);
	}}
>
	<p>Enter the 8 character code found in the bottom left corner of the sheet.</p>
	<!-- todo: little diagram showing where the code is? -->
	<!-- svelte-ignore a11y-autofocus -->
	<input
		class="enterManually"
		autofocus
		type="text"
		pattern="\w+"
		maxlength="8"
		placeholder="12345678"
		bind:value={manualCode}
	/>
</Modal>

<style lang="scss">
	.scanner {
		width: 100%;
		position: fixed;
		display: flex;
		justify-content: center;
		bottom: 0;
		left: 0;
		padding: 8px;
		box-sizing: border-box;
		transition: 360ms cubic-bezier(0.82, 0.03, 0.09, 1);
		opacity: 1;

		&.hidden {
			transform: translateY(calc(100% + 128px));
			pointer-events: none;
			opacity: 0;
		}

		& > div {
			width: 100%;
			max-width: 800px;
			height: 100%;
			aspect-ratio: 1;
			max-height: 60vh;
			background-color: var(--light);
			border-radius: 8px;
			overflow: hidden;
			position: relative;
			border: 2px solid var(--accent);
			box-sizing: border-box;
			> * {
				position: absolute;
				height: 100%;
				width: 100%;
				border-radius: 6px;
			}
			video {
				object-fit: cover;
			}
		}
	}
	.scannerOverlay {
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		padding: 16px;
		align-items: flex-end;
		box-sizing: border-box;
		&.showSquare {
			background-image: linear-gradient(
				to top,
				var(--light-translucent) 0%,
				100px,
				rgba(0, 0, 0, 0)
			);
			box-shadow: 0 0 0 16vw var(--qr-scanner-overlay-color) inset;
		}
		.scannerButtons {
			display: flex;
			width: 100%;
			justify-content: space-between;
		}
		.scannerMessage {
			font-size: 1em;
			font-weight: bold;
			width: 100%;
			margin: 0;
			text-align: center;
		}
	}

	.scanner.fallback > div {
		height: unset;
		aspect-ratio: unset;
		background-image: none;

		> * {
			position: unset;
			height: unset;
			width: unset;
		}
		p {
			width: 100%;
			font-weight: normal;
		}
	}

	input.enterManually {
		border-radius: 0;
		border: none;
		border-bottom: solid 2px var(--accent);
		outline: none;
	}
</style>
