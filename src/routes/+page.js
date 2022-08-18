
import { queryContentful } from 'logic/contentful.js';
const query = `{
	postCollection(order:sys_firstPublishedAt_DESC) {
		items {
			title
			contentText
			sys {
				publishedAt
			}
		}
	}
}`;
export async function load({ fetch }) {
	return { posts: (await queryContentful(fetch, query)).postCollection?.items };
}
