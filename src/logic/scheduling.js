export const DEFAULT_EVENT_DURATION_HOURS = 1;

export const addHoursToDate = (date, hours) => new Date(date.getTime() + hours * 60 * 60 * 1000);

export const eventIsFuture = (event) =>
	Date.now() <
	(event.endTime ?
		new Date(event.endTime)
	:	addHoursToDate(new Date(event.time), DEFAULT_EVENT_DURATION_HOURS)
	).getTime();
