<script context="module">
	import { writable } from 'svelte/store';
	const updateStore = writable(false);
	setInterval(() => updateStore.update((value) => !value), 30000); // ticker to periodically refresh relative times
</script>

<script>
	// inspired by react-moment
	import { DateTime, Duration } from 'luxon';

	const calendarStrings = {
		lastDay: "'Yesterday at' t",
		sameDay: "'Today at' t",
		nextDay: "'Tomorrow at' t",
		nextWeek: "EEEE 'at' t",
		sameElse: "MMMM d 'at' t", // more than 1 week away
	};
	function getCalendarFormat(myDateTime) {
		// https://stackoverflow.com/a/53715763/9985371
		var diff = myDateTime.diff(DateTime.local().startOf('day'), 'days').as('days');
		return myDateTime.toFormat(
			calendarStrings[
				diff < -6
					? 'sameElse'
					: diff < -1
					? 'lastWeek'
					: diff < 0
					? 'lastDay'
					: diff < 1
					? 'sameDay'
					: diff < 2
					? 'nextDay'
					: diff < 7
					? 'nextWeek'
					: 'sameElse'
			] || calendarStrings.sameElse
		);
	}

	export let date; // iso string
	export let format = 'EEEE, MMMM d, y \'at\' t';
	export let calendar = false; // use relative time strings like "today" instead of "monday", periodically refreshes
	export let duration = undefined; // displays time between date and duration
	export let fromNow = false; // use relative durations like "1 minute ago", periodically refreshes
	export let withTitle = false; // show original formatted date on hover

	date = DateTime.fromISO(date);
	let relative = calendar || fromNow;

	let timeString;
	const updateTimeString = () => {
		if (calendar) timeString = getCalendarFormat(date);
		else if (fromNow) timeString = date.toRelative();
	}
	if (relative) {
		updateTimeString();
		updateStore.subscribe(updateTimeString);
	}

	let durationString;
	if (duration) {
		let d = DateTime.fromISO(duration);
		d = date.diff(d, ['years', 'months', 'days', 'hours', 'minutes']);
		if (d.valueOf() < 0) d = d.negate();
		d = Duration.fromObject(Object.fromEntries(Object.entries(d.toObject()).filter(([_, val]) => val !== 0))); // remove 0s so they don't show up in the final string
		durationString = d.toHuman({ floor: true });
	}
</script>

<time datetime={date} title={withTitle && date.toFormat(format)}>
	{#if relative}
		{#key updateStore}
			{timeString}
		{/key}
	{:else if duration}
		{durationString}
	{:else}
		{date.toFormat(format)}
	{/if}
</time>
