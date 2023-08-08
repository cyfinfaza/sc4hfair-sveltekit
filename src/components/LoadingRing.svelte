<script>
	export let loading = true;
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<svg
	viewBox="0 0 100 100"
	fill="none"
	xmlns="http://www.w3.org/2000/svg"
	class="loadingRing"
	class:loading
	on:click={() => location.reload()}
>
	<path
		d="M100 50C100 43.4339 98.7067 36.9321 96.194 30.8658C93.6812 24.7995 89.9983 19.2876 85.3553 14.6447C80.7124 10.0017 75.2004 6.31876 69.1342 3.80602C63.0679 1.29329 56.5661 -2.87013e-07 50 0C43.4339 2.87013e-07 36.9321 1.29329 30.8658 3.80602C24.7995 6.31876 19.2876 10.0017 14.6447 14.6447C10.0017 19.2876 6.31876 24.7996 3.80602 30.8658C1.29329 36.9321 -5.74026e-07 43.4339 0 50L17.8865 50C17.8865 45.7828 18.7172 41.6069 20.331 37.7107C21.9449 33.8145 24.3103 30.2744 27.2923 27.2923C30.2744 24.3103 33.8145 21.9449 37.7107 20.331C41.6069 18.7172 45.7828 17.8865 50 17.8865C54.2172 17.8865 58.3931 18.7172 62.2893 20.331C66.1855 21.9449 69.7256 24.3103 72.7077 27.2923C75.6897 30.2744 78.0551 33.8145 79.669 37.7107C81.2828 41.6069 82.1135 45.7828 82.1135 50H100Z"
		style="fill: var(--text)"
	/>
</svg>

<style>
	.loadingRing {
		height: 0;
		width: 0;
		opacity: 0;
		animation: spin 0.5s infinite linear;
		transition: 120ms;
	}
	.loading {
		height: 1.2em;
		width: 1.2em;
		opacity: 1;
	}
	@keyframes spin {
		from {
			transform: rotate(-360deg);
		}

		to {
			transform: rotate(0deg);
		}
	}
</style>
