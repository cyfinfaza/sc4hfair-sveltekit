"""

Creates all the events in Contentful

python scheduleToContentful.py

"""

import contentful
import csv
import hashlib

contentTypeId = 'scheduledEvent'

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
							"id": contentful.yearTagId
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

		# this is unique enough and should prevent exact duplicates from being created, but still allow for the same event to be updated
		id = contentful.to_base62(int.from_bytes(hashlib.md5(f"{event['title']}{event['time']}".encode()).digest(), 'big'))

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

	newData = contentful.session.put(f'https://api.contentful.com/spaces/{contentful.spaceId}/environments/{contentful.environmentId}/entries/{id}', json=event['entry'], headers=headers)

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
entries = contentful.session.get(f'https://api.contentful.com/spaces/{contentful.spaceId}/environments/{contentful.environmentId}/entries?content_type={contentTypeId}&select=sys.id,sys.version&sys.archivedAt[exists]=false&limit=1000').json()
if entries['total'] > entries['limit']: print('todo: implement paging')

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
		contentful.session.delete(f'https://api.contentful.com/spaces/{contentful.spaceId}/environments/{contentful.environmentId}/entries/{id}/published', headers=headers)
		contentful.session.put(f'https://api.contentful.com/spaces/{contentful.spaceId}/environments/{contentful.environmentId}/entries/{id}/archived', headers=headers)

# create the rest that we aren't modifying
for id in tempEvents:
	print('creating', id)
	doEvent(id)

contentful.conditionalBulkPublish(publishPayload)