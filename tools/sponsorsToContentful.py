"""

Creates all the sponsors in Contentful

python sponsorsToContentful.py

"""

import contentful
import csv
import copy
from time import sleep

contentTypeId = 'sponsorSpot'

tierNameToSlug = {
	'Sky Level': 'sky',
	'Gold': 'gold',
	'Silver': 'silver',
	'Bronze': 'bronze',
	'Copper': 'copper',
	'Automobile': 'automobile',
	'Custom': 'custom',
	'Friends & Family': 'friends-family',
	'Business Card': 'business-card',
	'Inkind Donation': 'inkind'
}

allTierSlugs = list(tierNameToSlug.values())

# update enum
if not contentful.noPublish:
	ct = contentful.session.get(f'https://api.contentful.com/spaces/{contentful.spaceId}/environments/{contentful.environmentId}/content_types/{contentTypeId}').json()

	for field in ct['fields']:
		if field['id'] == 'tier':
			flag = False
			for valid in field['validations']:
				if 'in' in valid:
					valid['in'] = allTierSlugs
					flag = True
			if not flag:
				field['validations'].append({
					'in': allTierSlugs
				})
			break

	version = str(ct['sys']['version'])
	del ct['sys']

	req = contentful.session.put(f'https://api.contentful.com/spaces/{contentful.spaceId}/environments/{contentful.environmentId}/content_types/{contentTypeId}', json=ct, headers={
		'X-Contentful-Version': version,
	})

	version = str(req.json()['sys']['version'])

	# activate version
	req = contentful.session.put(f'https://api.contentful.com/spaces/{contentful.spaceId}/environments/{contentful.environmentId}/content_types/{contentTypeId}/published', headers={
		'X-Contentful-Version': version,
	})

newEntries = {}

with open('sponsors.csv') as csvfile:
	reader = csv.DictReader(csvfile)

	for sponsor in reader:
		if not sponsor.get('heading'): continue

		entry = {
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
				"tier": {
					"en-US": tierNameToSlug.get(sponsor['tierName'].strip())
				}
			}
		}

		heading = sponsor['heading'].strip()
		entry['fields']['heading'] = {
			"en-US": heading.strip()
		}

		if sponsor.get('link'):
			link = sponsor['link'].strip()
			if link and not link.startswith('http'):
				link = 'https://' + link
			entry['fields']['link'] = {
				"en-US": link
			}

		newEntries[heading] = {
			'heading': heading,
			'entry': entry,
		}

publishPayload = []
def doUpdate(heading):
	data = newEntries[heading]

	headers = {
		'X-Contentful-Content-Type': contentTypeId,
	}

	id = data.get('id')

	if id:
		# update
		headers['X-Contentful-Version'] = str(data['version'])

	if not contentful.noPublish:
		newData = getattr(contentful.session, 'put' if id else 'post')(f'https://api.contentful.com/spaces/{contentful.spaceId}/environments/{contentful.environmentId}/entries{f"/{id}" if id else ""}', json=data['entry'], headers=headers)

		if newData.status_code != 200 and newData.status_code != 201:
			print('error')
			print(data)
			print(newData.status_code, newData.headers)
			print(newData.text)
			print('---')
			return

		id = newData.json()['sys']['id']

		publishPayload.append({
			'sys': {
				'id': id,
				'type': 'Link',
				'linkType': 'Entry',
				'version': newData.json()['sys']['version'],
			}
		})

	sleep(0.2)

# get list of all previous entries
# the update api requires the version number of the entry to be updated
prevEntries = contentful.session.get(f'https://api.contentful.com/spaces/{contentful.spaceId}/environments/{contentful.environmentId}/entries?content_type={contentTypeId}&select=fields,sys.id,sys.version&sys.archivedAt[exists]=false&limit=1000').json()
print(prevEntries)

for entry in prevEntries['items']:
	id = entry['sys']['id']
	version = entry['sys']['version']
	heading = entry['fields']['heading']['en-US']

	if heading in newEntries:
		print('updating', heading)

		myEntry = entry
		for key in newEntries[heading]['entry']['fields']:
			myEntry['fields'][key] = copy.deepcopy(newEntries[heading]['entry']['fields'][key])
		newEntries[heading]['entry'] = myEntry

		newEntries[heading]['version'] = version
		newEntries[heading]['id'] = id

		doUpdate(heading)
		del newEntries[heading] # so when we try to create for the first time over every event
	else:
		print('archiving', heading, id)
		headers = {
			'X-Contentful-Version': str(version),
		}
		if not contentful.noPublish:
			contentful.session.delete(f'https://api.contentful.com/spaces/{contentful.spaceId}/environments/{contentful.environmentId}/entries/{id}/published', headers=headers)
			contentful.session.put(f'https://api.contentful.com/spaces/{contentful.spaceId}/environments/{contentful.environmentId}/entries/{id}/archived', headers=headers)

# create the rest that we aren't modifying
for heading in newEntries:
	print('creating', heading)
	doUpdate(heading)

contentful.conditionalBulkPublish(publishPayload)