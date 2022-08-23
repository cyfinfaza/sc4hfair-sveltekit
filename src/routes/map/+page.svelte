<script>
	import mapboxgl from 'mapbox-gl';
	import 'mapbox-gl/dist/mapbox-gl.css';
	import polylabel from 'polylabel';
	import { onMount, onDestroy } from 'svelte';

	import DateTime from 'components/DateTime.svelte';
	import Layout from 'components/Layout.svelte';
	import LinkButton from 'components/LinkButton.svelte';
	import Tabs from 'components/Tabs.svelte';
	import { theme } from 'logic/theming.js';
	import { eventIsFuture } from 'logic/scheduling.js';

	import mapbox_theme_light from 'data/mapbox-color-themes/theme-light';
	import mapbox_theme_dark from 'data/mapbox-color-themes/theme-dark';

	export let data;

	// the source/layer that contains our features
	const style = 'mapbox://styles/cyfinfaza/cl6idgfjs004x16p9y241804x',
		source = 'composite',
		sourceLayer = 'Fair_Tents_2022_with_names', // the name of the tileset
		sourceLayerId = 'Tents Flat'; // the name of the layer in the style that has the tileset

	mapboxgl.accessToken =
		'pk.eyJ1IjoiY3lmaW5mYXphIiwiYSI6ImNrYXBwN2N4ZTEyd3gycHF0bHhzZXIwcWEifQ.8Dx5dx27ity49fAGyZNzPQ';

	// location of the fair to center to
	const fairLng = -74.677043,
		fairLat = 40.577636,
		fairZoom = 16;

	// mapbox
	let /** @type {HTMLDivElement} */
		mapContainer,
		/** @type {import('mapbox-gl').Map} */
		map,
		isMapLoaded = false;

	// user locating
	/** @type {import('mapbox-gl').GeolocateControl} */
	let geolocate,
		trackUserLocationActive = false;

	// feature popup info
	let selectedFeature = null,
		previouslySelectedFeature = null,
		filteredEventData = [],
		filteredClubData = [];

	let easterEggCount = 0;

	const mapboxColorThemes = {
		light: mapbox_theme_light,
		dark: mapbox_theme_dark,
	};

	function changeTheme(theme) {
		const themeData = mapboxColorThemes[{ 'theme-light': 'light', 'theme-dark': 'dark' }[theme]];
		themeData.forEach((property) => {
			map.setPaintProperty(...property);
		});
	}

	$: if (isMapLoaded) {
		previouslySelectedFeature &&
			map.setFeatureState(
				{
					source: previouslySelectedFeature.source,
					id: previouslySelectedFeature.id,
					sourceLayer: previouslySelectedFeature.sourceLayer,
				},
				{
					click: false,
				}
			);
		if (selectedFeature) {
			map.setFeatureState(
				{
					source: selectedFeature.source,
					id: selectedFeature.id,
					sourceLayer: selectedFeature.sourceLayer,
				},
				{
					click: true,
				}
			);
			previouslySelectedFeature = selectedFeature;
			filteredEventData = data.events.filter(
				(event) => event.tent === selectedFeature?.properties.slug && eventIsFuture(event)
			);
			filteredClubData = data.clubs.filter(
				(club) => club.tent === selectedFeature?.properties.slug
			);
		} else {
			previouslySelectedFeature = null;
		}
	}

	function selectFeature(slug) {
		let query = map.querySourceFeatures(source, {
			sourceLayer: sourceLayer,
			filter: ['==', 'slug', slug], // check feature slug
		});
		if (query.length !== 0) {
			// assuming that the biggest id is actually the one shown because otherwise i have no idea how to get the correct one
			let element = query.reduce((a, b) => (a.id > b.id ? a : b));
			console.log(element, query);

			map.flyTo({
				center: polylabel(element.geometry.coordinates), // use the center of the feature
				zoom: 18.5,
				speed: 2.7, // this is done once on page load so make it go fast
			});
			map.once('moveend', () => {
				selectedFeature = {
					source,
					sourceLayer,
					...element,
				};
			});
		} else {
			console.warn('No feature found for slug:', toLocate);
		}
	}
	onMount(() => {
		if (map) return; // Initialize map only once
		map = new mapboxgl.Map({
			container: mapContainer,
			style,
			center: [fairLng, fairLat],
			zoom: fairZoom,
			attributionControl: false,
		});

		map.on('load', (_) => {
			isMapLoaded = true;
			changeTheme($theme);
			theme.subscribe((next) => {
				changeTheme(next);
			});

			// Locate a tent by its slug
			let toLocate = new URLSearchParams(window.location.search).get('locate');
			if (toLocate) selectFeature(toLocate);
		});

		window.map = map;

		geolocate = new mapboxgl.GeolocateControl({
			positionOptions: {
				enableHighAccuracy: true,
			},
			trackUserLocation: true,
			showUserHeading: true,
		});

		geolocate.on('trackuserlocationstart', () => {
			trackUserLocationActive = true;
		});
		geolocate.on('trackuserlocationend', () => {
			trackUserLocationActive = false;
		});

		map.addControl(geolocate);

		const scale = new mapboxgl.ScaleControl({
			unit: 'imperial',
		});
		map.addControl(scale);

		map.on('click', sourceLayerId, (e) => {
			const feature = e.features[0];
			console.log(selectedFeature, feature);
			selectedFeature = feature;
		});
	});
</script>

<Layout title="Map" noPadding noHeaderPadding fixedHeightContent fullWidth>
	<div class="controls">
		<LinkButton
			label="Center on fair"
			icon="place"
			on:click={() => {
				easterEggCount++;
				map.flyTo({
					center: [fairLng, fairLat],
					zoom: fairZoom,
				});
			}}
			lightFont
			acrylic
		/>
		<LinkButton
			label={trackUserLocationActive ? 'Stop locating me' : 'Locate me'}
			icon={trackUserLocationActive ? 'location_disabled' : 'my_location'}
			on:click={() => {
				geolocate.trigger();
			}}
			lightFont
			acrylic
		/>
	</div>
	<div class="mapContainer" class:easterEgg={easterEggCount >= 50} bind:this={mapContainer} />
	<div
		class="tentInfo"
		class:hidden={!selectedFeature}
		aria-hidden={!selectedFeature}
		class:short={filteredEventData.length === 0 && filteredClubData.length === 0}
	>
		<div>
			<h2 class="tentInfoHeading">
				{selectedFeature?.properties.name || selectedFeature?.properties.slug || '-'}
				<LinkButton
					label="Close"
					icon="close"
					on:click={() => {
						selectedFeature = null;
					}}
					acrylic
				/>
			</h2>
			{#key selectedFeature}
				<Tabs
					tabs={[
						{ key: 'events', enabled: filteredEventData.length > 0, name: 'Events' },
						{ key: 'clubs', enabled: filteredClubData.length > 0, name: 'Clubs' },
					]}
					let:key
				>
					{#if key === 'events'}
						{#if filteredEventData.length}
							<ul>
								{#each filteredEventData as event}
									<li key={event.id}>
										<a href={'/schedule#' + event.id}>{event.title}</a>
										<small>(<DateTime date={event.time} />)</small>
									</li>
								{/each}
							</ul>
						{:else}
							<p>No future events found</p>
						{/if}
					{:else if key === 'clubs'}
						{#if filteredClubData.length}
							<ul>
								{#each filteredClubData as club}
									<li key={club.slug}>
										<a href={'/clubs#' + club.slug}>{club.name}</a>
									</li>
								{/each}
							</ul>
						{:else}
							<p>No clubs found</p>
						{/if}
					{/if}
				</Tabs>
			{/key}
		</div>
	</div>
</Layout>

<style lang="scss">
	.mapContainer {
		width: 100%;
		height: 100%;
		overflow: hidden;
	}

	.controls {
		position: absolute;
		width: 100%;
		box-sizing: border-box;
		padding: 8px;
		margin-top: var(--nav-height);
		display: flex;
		gap: 8px;
		flex-direction: column;
		align-items: flex-end;
		/* pointer-events: none; */

		> :global(*) {
			z-index: 10;
		}
	}

	.tentInfo {
		position: fixed;
		bottom: 0;
		width: 100%;
		// padding: 8px;
		display: flex;
		flex-direction: column;
		align-items: center;
		box-sizing: border-box;
		z-index: 11;
		transition: 360ms cubic-bezier(0.82, 0.03, 0.09, 1);
		padding: 8px;

		&.hidden {
			transform: translateY(calc(100% + 128px));
			// opacity: 0;
			pointer-events: none;
		}

		&.short > * {
			height: auto;
		}

		> * {
			background-color: var(--light-blur);
			backdrop-filter: var(--backdrop-blur);
			// background: var(--light);
			border-radius: 8px;
			width: 100%;
			max-width: 500px;
			padding: 16px;
			display: flex;
			flex-direction: column;
			gap: 8px;
			height: 300px;
			max-height: 100%;
			box-sizing: border-box;
			overflow: auto;
			> * {
				margin: 0;
			}
		}
	}

	.tentInfoHeading {
		display: flex;
		justify-content: space-between;
		gap: 12px;
		align-items: center;
		width: 100%;
	}

	// @media screen and (max-width: 700px) {
	// 	.tentInfo {
	// 		padding: 0px;
	// 		> * {
	// 			max-width: 100%;
	// 			border-radius: 0;
	// 		}
	// 	}
	// }

	.easterEgg :global(canvas) {
		background-color: red;
		animation: hueRotate 3s infinite;
	}

	@keyframes hueRotate {
		0% {
			filter: hue-rotate(0deg);
		}
		100% {
			filter: hue-rotate(360deg);
		}
	}

	:global {
		.mapboxgl-map {
			font-family: inherit;
		}

		.mapboxgl-ctrl-scale {
			background-color: var(--light-blur);
			backdrop-filter: var(--backdrop-blur);
			border-radius: 5px 5px 0 0;
			color: var(--text);
			border: none;
			border-bottom: 2px solid var(--text);
		}

		.mapboxgl-ctrl-top-right {
			display: none;
		}
	}
</style>
