<script>
	import mapboxgl from 'mapbox-gl';
	import 'mapbox-gl/dist/mapbox-gl.css';
	import polylabel from 'polylabel';
	import { onMount } from 'svelte';

	import DateTime from 'components/DateTime.svelte';
	import Layout from 'components/Layout.svelte';
	import LinkButton from 'components/LinkButton.svelte';
	import Tabs from 'components/Tabs.svelte';
	import { eventIsFuture } from 'logic/scheduling.js';

	export let data;

	// the source/layer that contains our features
	const style = 'mapbox://styles/cyfinfaza/clksqsyk001vj01p51e7m6ode',
		source = 'composite',
		sourceLayer = 'Fair_Tents_2023_with_names', // the name of the tileset
		sourceLayerId = 'Tents Flat'; // the name of the layer in the style that has the tileset

	mapboxgl.accessToken =
		'pk.eyJ1IjoiY3lmaW5mYXphIiwiYSI6ImNrYXBwN2N4ZTEyd3gycHF0bHhzZXIwcWEifQ.8Dx5dx27ity49fAGyZNzPQ';

	// location of the fair to center to
	const fairLng = -74.677043,
		fairLat = 40.577636,
		fairZoom = 17;

	// mapbox
	let /** @type {HTMLDivElement} */ mapContainer,
		/** @type {mapboxgl.Map} */ map,
		isMapLoaded = false;

	// user locating
	let /** @type {mapboxgl.GeolocateControl} */ geolocate,
		trackUserLocationActive = false,
		trackUserLocationRecenter = false;

	// feature popup info
	let /** @type {mapboxgl.MapboxGeoJSONFeature} */ selectedFeature = null,
		/** @type {mapboxgl.MapboxGeoJSONFeature} */ previouslySelectedFeature = null,
		filteredEventData = null,
		filteredClubData = null;

	let easterEggCount = 0;

	$: try {
		if (isMapLoaded) {
			if (previouslySelectedFeature) {
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
			}
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

				let slug = selectedFeature?.properties.slug;
				console.log(data);
				filteredEventData = data.eventsByTent[slug]?.filter((event) => eventIsFuture(event));
				filteredClubData = data.clubsByTent[slug];
			} else {
				previouslySelectedFeature = null;
			}
		}
	} catch (e) {
		console.error(e);
		if (confirm('Unhandled error while selecting feature, reload?')) location?.reload();
	}

	async function selectFeature(slug) {
		let zoom = map.getZoom();
		map.setZoom(13);
		await new Promise((resolve) => setTimeout(resolve, 200));
		let query = map.querySourceFeatures(source, {
			sourceLayer: sourceLayer,
			filter: ['==', 'slug', slug], // check feature slug
		});
		map.setZoom(zoom);
		if (query.length !== 0) {
			console.log(query);
			// assuming that the biggest id is actually the one shown because otherwise i have no idea how to get the correct one
			let element = query.reduce((a, b) => (a.id > b.id ? a : b));
			console.log(element, query);

			map.flyTo({
				center:
					typeof element.geometry.coordinates[0] === 'number'
						? element.geometry.coordinates
						: polylabel(element.geometry.coordinates), // use the center of the feature
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
			console.warn('No feature found for slug:', slug);
		}
	}

	onMount(() => {
		if (map) return; // Initialize map only once

		let toLocate = new URLSearchParams(window.location.search).get('locate');

		map = new mapboxgl.Map({
			container: mapContainer,
			style,
			center: [fairLng, fairLat],
			zoom: toLocate ? 15 : fairZoom,
			attributionControl: false,
		});

		map.on('load', (_) => {
			isMapLoaded = true;

			if (toLocate) selectFeature(toLocate);
		});

		map.on('click', [sourceLayerId, 'Labels'], (e) => {
			const feature = e.features[0];
			console.log(selectedFeature, feature);
			selectedFeature = feature;
		});

		window.map = map;
		window.selectFeature = selectFeature;

		geolocate = new mapboxgl.GeolocateControl({
			positionOptions: {
				enableHighAccuracy: true,
			},
			trackUserLocation: true,
			showUserHeading: true,
		});
		geolocate.on('trackuserlocationstart', () => {
			trackUserLocationActive = true;
			trackUserLocationRecenter = false;
		});
		geolocate.on('trackuserlocationend', () => {
			// this event is fired when the map moves as the button turns into one that recenters on the user
			if (geolocate._watchState === 'OFF') {
				trackUserLocationActive = false; // actually stopping for realz
				trackUserLocationRecenter = false;
			} else trackUserLocationRecenter = true;
		});
		map.addControl(geolocate);

		const scale = new mapboxgl.ScaleControl({
			unit: 'imperial',
		});
		map.addControl(scale);

		return () => map.remove();
	});
</script>

<Layout title="Map" noPadding noHeaderPadding fixedHeightContent fullWidth forceTheme="dark">
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
			label={trackUserLocationRecenter
				? 'Center on me'
				: trackUserLocationActive
				? 'Stop locating me'
				: 'Locate me'}
			icon={trackUserLocationRecenter
				? 'gps_not_fixed'
				: trackUserLocationActive
				? 'gps_off'
				: 'gps_fixed'}
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
		class:short={!filteredEventData?.length && !filteredClubData?.length}
	>
		<div>
			<h2>
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
						{ key: 'events', enabled: filteredEventData?.length > 0, name: 'Events' },
						{ key: 'clubs', enabled: filteredClubData?.length > 0, name: 'Clubs' },
					]}
					let:key
				>
					{#if key === 'events'}
						{#if filteredEventData?.length}
							<ul>
								{#each filteredEventData as event}
									<li key={event.id}>
										<a href={'/schedule#' + event.id}>{event.title}</a>
										<small>(<DateTime date={event.time} calendar />)</small>
									</li>
								{/each}
							</ul>
						{:else}
							<p>No future events found</p>
						{/if}
					{:else if key === 'clubs'}
						{#if filteredClubData?.length}
							<ul>
								{#each filteredClubData as club}
									<li key={club.slug}>
										<a href={'/club/' + club.slug}>{club.name}</a>
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

		pointer-events: none;
		> * {
			pointer-events: auto;
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

		h2 {
			display: flex;
			justify-content: space-between;
			gap: 12px;
			align-items: center;
			width: 100%;
		}
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
