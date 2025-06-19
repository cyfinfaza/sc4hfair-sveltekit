<script module>
	import { writable } from 'svelte/store';
	const updateStore = writable(false);
	setInterval(() => updateStore.update((value) => !value), 1000); // ticker to periodically refresh relative times
</script>

<script lang="ts">
	// inspired by react-moment
	import { DateTime, Duration } from 'luxon';

	let {
		date,
		format = "EEEE, MMMM d, y 'at' t",
		calendar = false,
		duration = undefined,
		fromNow = false,
		withTitle = false,
	}: {
		/** iso string */
		date: string;

		/** displays time between date and duration */
		duration?: string;

		format?: string;
		/** use relative time strings like "today" instead of "monday", periodically refreshes */
		calendar?: boolean;
		/** use relative durations like "1 minute ago", periodically refreshes */
		fromNow?: boolean;

		/** show original formatted date on hover */
		withTitle?: boolean;
	} = $props();

	const calendarStrings = {
		lastDay: "'Yesterday at' t",
		sameDay: "'Today at' t",
		nextDay: "'Tomorrow at' t",
		nextWeek: "EEEE 'at' t",
		sameElse: "MMMM d 'at' t", // more than 1 week away
	};

	function getCalendarFormat(myDateTime: DateTime) {
		// https://stackoverflow.com/a/53715763/9985371
		var diff = myDateTime.diff(DateTime.local().startOf('day'), 'days').as('days');
		return myDateTime.toFormat(
			calendarStrings[
				diff < -6 ? 'sameElse'
					// : diff < -1 ? 'lastWeek'
				: diff < 0 ? 'lastDay'
				: diff < 1 ? 'sameDay'
				: diff < 2 ? 'nextDay'
				: diff < 7 ? 'nextWeek'
				: 'sameElse'
			] || calendarStrings.sameElse
		);
	}

	let relative = $derived(calendar || fromNow);

	let dateObj = $derived(DateTime.fromISO(date));

	let durationString = $derived.by(() => {
		if (duration) {
			let d = DateTime.fromISO(duration);
			if (d.isValid === true) {
				let diffObj = dateObj.diff(d, ['years', 'months', 'days', 'hours', 'minutes']);
				if (d.valueOf() < 0) diffObj = diffObj.negate();
				let durationObj = Duration.fromObject(
					Object.fromEntries(Object.entries(diffObj.toObject()).filter(([, val]) => val !== 0))
				); // remove 0s so they don't show up in the final string
				durationString = durationObj.toHuman();
			}
		}
		return '';
	});

	let timeString = $derived.by(() => {
		if (relative) {
			$updateStore; // trigger reactivity

			if (calendar) return getCalendarFormat(dateObj);
			else if (fromNow) return dateObj.toRelative();
		} else {
			return dateObj.toFormat(format);
		}
	});
</script>

<time datetime={dateObj?.toISO()} title={withTitle ? dateObj?.toFormat(format) : null}>
	{#if duration}
		{durationString}
	{:else}
		{timeString}
	{/if}
</time>
