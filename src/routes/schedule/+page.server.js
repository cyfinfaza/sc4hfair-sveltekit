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
			tent
		}
	}
}`;

export async function load() {
	const resp = await queryContentful(query);
	return { events: resp.scheduledEventCollection?.items };
}
