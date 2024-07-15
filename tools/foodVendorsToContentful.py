"""

Creates all the food vendors and pricing in Contentful

python foodVendorsToContentful.py

"""

import contentful
import csv
import re
from uuid import uuid4

contentTypeId = 'foodVendor'

newVendors = {}

with open('foodVendors.csv') as csvfile:
	# remember to:
	# - remove any extra heading above the row names
	# - make sure row names match
	# - clean up typos
	# - clean up prices (especially when multiple listed)
	reader = csv.DictReader(csvfile)

	for line in reader:
		if not line['name']: continue
		name = re.sub(r'\b4-?H\b', '4‑H',
			re.sub(r'\s{2,}', ' ',
			re.sub(r'\s*/\s*', '/',
			line['name'].strip())))

		if name not in newVendors:
			newVendors[name] = {
				"metadata": {
					"tags": [
						{
							"sys": {
								"type": "Link",
								"linkType": "Tag",
								"id": contentful.yearTagId
							}
						}
					]
				},
				"fields": {
					"name": {
						"en-US": name
					},
					"items": {
						"en-US": []
					}
				}
			}

		if not line['item']: continue

		newVendors[name]['fields']['items']['en-US'].append({
			"id": str(uuid4()), # https://github.com/davidfateh/repeater-app/blob/main/src/components/Field.tsx#L31
			"key": line['item'].strip(),
			"value": line['price'].strip()
		})

# get list of all previous entries
# the update api requires the version number of the entry to be updated
entries = contentful.session.get(f'https://api.contentful.com/spaces/{contentful.spaceId}/environments/{contentful.environmentId}/entries?content_type={contentTypeId}&select=sys.id,sys.version,fields.name&sys.archivedAt[exists]=false&limit=1000').json()
if entries['total'] > entries['limit']: print('todo: implement paging')

previousData = {}
newNames = newVendors.keys()
for entry in entries['items']:
	name = entry['fields']['name']['en-US']
	id = entry['sys']['id']
	version = entry['sys']['version']

	previousData[name] = (id, version)

	if name not in newNames:
		print('archiving', name)
		contentful.session.delete(f'https://api.contentful.com/spaces/{contentful.spaceId}/environments/{contentful.environmentId}/entries/{id}/published', headers={
			'X-Contentful-Version': str(version),
		})
		contentful.session.put(f'https://api.contentful.com/spaces/{contentful.spaceId}/environments/{contentful.environmentId}/entries/{id}/archived', headers={
			'X-Contentful-Version': str(version),
		})

publishPayload = []

for vendor in newVendors:
	print('updating', vendor)

	entryId = None
	headers = {
		'X-Contentful-Content-Type': contentTypeId,
	}
	if vendor in previousData:
		entryId = previousData[vendor][0]
		headers['X-Contentful-Version'] = str(previousData[vendor][1])
	else:
		print('creating', vendor)
		entryId = contentful.new_id()

	newData = contentful.session.put(f'https://api.contentful.com/spaces/{contentful.spaceId}/environments/{contentful.environmentId}/entries/{entryId}', json=newVendors[vendor], headers=headers)

	if newData.status_code != 200 and newData.status_code != 201:
		print('error')
		print(newData.status_code, newData.headers)
		print(newData.text)
		print('---')
		continue
	publishPayload.append({
		'sys': {
			'id': entryId,
			'type': 'Link',
			'linkType': 'Entry',
			'version': newData.json()['sys']['version'],
		}
	})

contentful.conditionalBulkPublish(publishPayload)