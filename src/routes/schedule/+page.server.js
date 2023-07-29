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
	/** @type {str[]} */
	const events = resp.scheduledEventCollection?.items;

	const eventTentsList = ['All', ...new Set(events.map((event) => event.tent))].filter(
		(tent) => tent && tent !== '---'
	);

	return { events, eventTentsList };
}
