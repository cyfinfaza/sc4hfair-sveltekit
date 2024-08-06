export const DEFAULT_EVENT_DURATION_HOURS = 1;

/**
 * @param {Date} date
 * @param {number} hours
 */
export const addHoursToDate = (date, hours) => new Date(date.getTime() + hours * 60 * 60 * 1000);

/** @param {Object & { time: string; endTime?: string | null }} event */
export const eventIsFuture = (event) =>
	Date.now() <
	(event.endTime ?
		new Date(event.endTime)
	:	addHoursToDate(new Date(event.time), DEFAULT_EVENT_DURATION_HOURS)
	).getTime();
