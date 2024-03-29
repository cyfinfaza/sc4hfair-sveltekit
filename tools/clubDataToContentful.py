"""

Updates and publishes club data in Contentful

python clubDataToContentful.py

possible arguments:
	--no-publish - don't publish the entries after updating them

"""

import config
import json
import requests
import sys

contentTypeId = 'club'

noPublish = '--no-publish' in sys.argv

data = json.load(open('clubData.json'))
allSlugs = [club['slug'] for club in data]

session = requests.Session()
session.headers.update({
	'Authorization': 'Bearer ' + config.cmaToken,
	'Content-Type': 'application/vnd.contentful.management.v1+json',
})

# get list of all previous entries
# the update api requires the version number of the entry to be updated
# we can grab them all in bulk at the start
entries = session.get(f'https://api.contentful.com/spaces/{config.spaceId}/environments/{config.environmentId}/entries?content_type={contentTypeId}&select=sys.id,sys.version,fields.slug&sys.archivedAt[exists]=false').json()

if entries['total'] > entries['limit']:
	print('todo: implement paging')

previousData = {}
for entry in entries['items']:
	slug = entry['fields']['slug']['en-US']
	id = entry['sys']['id']
	version = entry['sys']['version']

	previousData[slug] = (id, version)

	if slug not in allSlugs:
		print('archiving', slug)
		session.delete(f'https://api.contentful.com/spaces/{config.spaceId}/environments/{config.environmentId}/entries/{id}/published', headers={
			'X-Contentful-Version': str(version),
		})
		req = session.put(f'https://api.contentful.com/spaces/{config.spaceId}/environments/{config.environmentId}/entries/{id}/archived', headers={
			'X-Contentful-Version': str(version),
		})

publishPayload = []

for club in data:
	# if club['slug'] != '4h-computers': continue # for testing

	print('updating', club['slug'])
	entry = {
		"fields": {
			"name": {
				"en-US": club['name']
			},
			"slug": {
				"en-US": club['slug']
			},
			"listingWebsite": {
				"en-US": club['listingWebsite'] if 'listingWebsite' in club else ('https://4histops.org/' + club['slug'])
			}
		}
	}

	for key in ['description', 'meetingLocation', 'meetingWhen', 'grades', 'clubWebsite', 'tent']:
		if key in club:
			entry['fields'][key] = {
				"en-US": club[key]
			}

	# data that exists in contentful but not the file will be overwritten
	# we'd need to do patching to get around that, but it's fine ig

	entryId = club['slug']

	headers = {
		'X-Contentful-Content-Type': contentTypeId,
	}
	if club['slug'] in previousData:
		entryId = previousData[club['slug']][0]
		headers['X-Contentful-Version'] = str(previousData[club['slug']][1])
	
	# print(club['slug'], entry, headers)

	newData = session.put(f'https://api.contentful.com/spaces/{config.spaceId}/environments/{config.environmentId}/entries/{entryId}', json=entry, headers=headers)

	if newData.status_code != 200 and newData.status_code != 201:
		print('error')
		print(entry)
		print(newData.status_code, newData.headers)
		print(newData.text)
		print('---')
		# readd the club to try again later
		data.append(club)
		continue

	publishPayload.append({
		'sys': {
			'id': entryId,
			'type': 'Link',
			'linkType': 'Entry',
			'version': newData.json()['sys']['version'],
		}
	})

if not noPublish and len(publishPayload) > 0:
	bulkReq = session.post(f'https://api.contentful.com/spaces/{config.spaceId}/environments/{config.environmentId}/bulk_actions/publish', json={
		'entities': {
			'items': publishPayload,
		},
	})

	print('bulk publish status', bulkReq.status_code, bulkReq.json()['sys']['status'], bulkReq.json())