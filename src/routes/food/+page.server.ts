import { queryContentful } from 'logic/contentful';

const query = `{
	foodVendorCollection(order: name_ASC) {
		items {
			name
			items
		}
	}
}`;

export interface FoodVendor {
	name: string;
	items: { key: string; value: string; id: string }[];
}

let loadedData = false,
	foodVendors: FoodVendor[] = [];

export const load: import('./$types').PageServerLoad = async () => {
	if (!loadedData) {
		const resp: { foodVendorCollection: { items: FoodVendor[] } } = await queryContentful(query);

		foodVendors = resp.foodVendorCollection?.items;

		loadedData = true;
	}

	return { foodVendors };
};
