<script>
	// If you look at the source code to cheat and get to the end, then congrats
	// I'm not going to try and do a fancy thing or whatever to prevent it
	// You win, come join the 4-H Computer Club

	import QrScanner from 'qr-scanner';
	import ClueBox from './ClueBox.svelte';
	import Layout from 'components/Layout.svelte';
	import LinkButton from 'components/LinkButton.svelte';
	import shData from 'data/shClues.json';
	import { browser } from '$app/environment';
	import { onMount, setContext } from 'svelte';
	import { writable } from 'svelte/store';
	import Modal from 'components/Modal.svelte';

	const clues = shData.clues;

	const getIndexFromCode = (code) => clues.findIndex((clue) => clue.code === code);
	const getOffsetIndexFromCode = (code) => getIndexFromCode(code) + 1;

	const storageKeyPrefix = `sh_2023_`;

	let atIndex = writable(0);
	$: if ($atIndex > 0) localStorage.setItem(storageKeyPrefix + 'code', clues[$atIndex - 1].code);

	let hintsUsed = writable([]);
	$: if ($hintsUsed.length)
		localStorage.setItem(storageKeyPrefix + 'hints', JSON.stringify($hintsUsed));

	setContext('sh', {
		atIndex,
		hintsUsed,
		addHintUsed: (code) => ($hintsUsed = [...$hintsUsed, code]),
		clues,
		startScanning: () => (scanning = true),
	});

	let videoElement,
		qrScanner,
		compatible = false,
		scanning = false,
		scannerMessage = '';

	onMount(async () => {
		if (browser) {
			let tmpIndex = getOffsetIndexFromCode(localStorage.getItem(storageKeyPrefix + 'code'));
			if (tmpIndex) $atIndex = tmpIndex;

			let hints = JSON.parse(localStorage.getItem(storageKeyPrefix + 'hints'));
			if (hints && hints.length > 0) $hintsUsed = hints;

			checkCode(new URLSearchParams(window.location.search).get('code'), true); // Code from a scanned URL bringing them here
			window.history.replaceState(null, null, window.location.pathname);
		}

		try {
			compatible = typeof navigator === 'object' && (await QrScanner.hasCamera());
		} catch (e) {}
		if (!compatible) return;

		try {
			qrScanner = new QrScanner(
				videoElement,
				({ data: code }) => {
					// Extract the code from a URL
					try {
						let tempCode = new URLSearchParams(new URL(code).search).get('code');
						if (typeof tempCode === 'string') code = tempCode;
					} catch (e) {} // if it fails, it isn't a URL with a code
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

		() => qrScanner.destroy();
	});

	$: if (compatible) {
		if (scanning)
			qrScanner.start().catch((e) => {
				console.error(e);
				compatible = false;
			});
		else {
			scannerMessage = '';
			qrScanner.stop();
		}
	}

	let scannerMessageTimeout;

	function checkCode(code, fromUrl = false) {
		let index = getIndexFromCode(code);
		console.table({ fromUrl, $atIndex });
		const clueIsInFalseList = shData.falseCodes.includes(code);
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
		}
		if (scannerMessageTimeout) clearTimeout(scannerMessageTimeout);
		scannerMessageTimeout = setTimeout(() => (scannerMessage = ''), 10000);
		if (!clues[$atIndex]) return;
		console.table({
			code,
			index: index,
			'current code': clues[$atIndex].code,
			'current index': $atIndex,
			'current clue': clues[$atIndex].clue,
		});
	}

	let showEnterManuallyPrompt = false,
		manualCode = '';
</script>

<Layout title="Scavenger Hunt">
	<div class="center">
		<h1>2023 Scavenger Hunt</h1>
		<p>
			Welcome to the 4‑H Fair Scavenger Hunt! Each clue will lead you to a QR Code, and when you
			scan it, it will unlock the next clue. The last clue will lead you to your prize: a $1
			<a href="/map?locate=food">food</a> voucher for the fair and maybe something else...
		</p>
		<p>
			If you're stuck on a clue, try looking at the <a href="/map">fair map</a>, talking to other
			4‑Hers, or searching for information online. You can get a hint on each clue if you're stuck,
			but if you choose to you won't get a "perfect score". Go to <a href="/settings">settings</a> to
			reset the scavenger hunt, though only one prize may be claimed per person.
		</p>
		<p>Hints used: {$hintsUsed.length}</p>
		{#each clues as _, index}
			<ClueBox {index} />
		{/each}
		<ClueBox winner />
	</div>

	<!-- this div needs to always be rendered so the qr library doesn't die -->
	<div
		class="scanner"
		class:hidden={!scanning || !compatible}
		aria-hidden={!scanning || compatible}
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
				<p>
					The scavenger hunt recommends a QR scanner. Check that your browser is allowing the app
					camera access to use the built-in one, or use an external scanner.
				</p>
				<p>Alternatively, you can manually enter the code:</p>
				<LinkButton
					label="Enter manually"
					icon="keyboard"
					on:click={() => (showEnterManuallyPrompt = true)}
				/>
			</div>
		</div>
	</div>
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

		&.hidden {
			transform: translateY(calc(100% + 128px));
			pointer-events: none;
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
