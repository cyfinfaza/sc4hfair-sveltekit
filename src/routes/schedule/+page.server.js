import { queryContentful } from 'logic/contentful.js';

// big limit to make sure we get all events!!, default is 100 but we have 200+ events
const query = `{
	scheduledEventCollection(order: time_ASC, limit: 500) {
		items {
			sys {
				id
			}
			title
			time
			endTime
			tent
			near
		}
	}
}`;

export async function load() {
	const resp = await queryContentful(query);
	const events = resp.scheduledEventCollection?.items;

	/** @type {string[]} */
	const eventTentsList = ['All', ...new Set(events.map((event) => event.tent))].filter(Boolean);

	return { events, eventTentsList };
}
