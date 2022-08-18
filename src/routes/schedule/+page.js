import { queryContentful } from 'logic/contentful.js';

const query = `{
	scheduledEventCollection(order:sys_firstPublishedAt_DESC) {
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

export async function load({ fetch }) {
	const resp = await queryContentful(fetch, query);
	return { events: resp.scheduledEventCollection?.items };
}
