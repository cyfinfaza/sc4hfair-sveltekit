"""

Creates all the events in Contentful

python scheduleToContentful.py

"""

import config
import sys
import csv
import requests
import hashlib

contentTypeId = 'scheduledEvent'

noPublish = '--no-publish' in sys.argv

session = requests.Session()
session.headers.update({
	'Authorization': 'Bearer ' + config.cmaToken,
	'Content-Type': 'application/vnd.contentful.management.v1+json',
})

tempEvents = {}

with open('schedule.csv') as csvfile:
	reader = csv.DictReader(csvfile)

	for event in reader:
		if not event['title']: continue # skip header rows

		entry = {
			"metadata": {
				"tags": [
					{
						"sys": {
							"type": "Link",
							"linkType": "Tag",
							"id": "2023"
						}
					}
				]
			},
			"fields": {
				"near": {
					"en-US": True if event['near'] == 'true' else False
				},
			}
		}

		for key in ['title', 'time', 'endTime', 'tent']:
			if event.get(key):
				entry['fields'][key] = {
					"en-US": event[key]
				}
		
		# this is unique enough and should prevent exact duplicates
		id = hashlib.md5(f"{event['title']}{event['time']}".encode()).hexdigest()

		tempEvents[id] = {
			'entry': entry,
		}
		print(tempEvents[id])

		# print(id, entry)

publishPayload = []
# handles updating or creating an event
def doEvent(id):
	event = tempEvents[id]

	headers = {
		'X-Contentful-Content-Type': contentTypeId,
	}

	if 'version' in event:
		# update
		headers['X-Contentful-Version'] = str(event['version'])

	newData = session.put(f'https://api.contentful.com/spaces/{config.spaceId}/environments/{config.environmentId}/entries/{id}', json=event['entry'], headers=headers)

	if newData.status_code != 200 and newData.status_code != 201:
		print('error')
		print(entry)
		print(newData.status_code, newData.headers)
		print(newData.text)
		print('---')
		return

	publishPayload.append({
		'sys': {
			'id': id,
			'type': 'Link',
			'linkType': 'Entry',
			'version': newData.json()['sys']['version'],
		}
	})

# get list of all previous entries
# the update api requires the version number of the entry to be updated
entries = session.get(f'https://api.contentful.com/spaces/{config.spaceId}/environments/{config.environmentId}/entries?content_type={contentTypeId}&select=sys.id,sys.version&sys.archivedAt[exists]=false&limit=1000').json()

for entry in entries['items']:
	id = entry['sys']['id']
	version = entry['sys']['version']

	if id in tempEvents:
		print('updating', id)
		tempEvents[id]['version'] = version
		doEvent(id)
		del tempEvents[id] # so when we try to create for the first time over every event
	else:
		print('archiving', id)
		headers = {
			'X-Contentful-Version': str(version),
		}
		session.delete(f'https://api.contentful.com/spaces/{config.spaceId}/environments/{config.environmentId}/entries/{id}/published', headers=headers)
		session.put(f'https://api.contentful.com/spaces/{config.spaceId}/environments/{config.environmentId}/entries/{id}/archived', headers=headers)

# create the rest that we aren't modifying
for id in tempEvents:
	print('creating', id)
	doEvent(id)

if not noPublish and len(publishPayload) > 0:
	bulkReq = session.post(f'https://api.contentful.com/spaces/{config.spaceId}/environments/{config.environmentId}/bulk_actions/publish', json={
		'entities': {
			'items': publishPayload,
		},
	})

	print('bulk publish status', bulkReq.status_code, bulkReq.text)