import { queryContentful } from 'logic/contentful.js';

const query = `{
	scheduledEventCollection(order:sys_firstPublishedAt_DESC, where: {time_gt: "${new Date().toISOString()}"}) {
		items {
			sys {
				id
			}
			title
			time
			tent
		}
	}
	clubCollection {
		items {
			name
			slug
			tent
		}
	}
}`;

export async function load({ fetch }) {
	const resp = await queryContentful(fetch, query);
	return { events: resp.scheduledEventCollection?.items, clubs: resp.clubCollection?.items };
}
