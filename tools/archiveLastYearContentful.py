import contentful
import requests

(webhookPreviousActive, webhookUrl) = contentful.setWebhookActive(contentful.vercelWebhookId, False)
print('webhook disabled')

# get list of all previous entries
# the update api requires the version number of the entry to be updated
entries = []

for contentTypeId in ['scheduledEvent', 'post']:
	res = contentful.session.get(f'https://api.contentful.com/spaces/{contentful.spaceId}/environments/{contentful.environmentId}/entries?content_type={contentTypeId}&select=sys.id,sys.version&sys.archivedAt[exists]=false&metadata.tags.sys.id[in]={contentful.lastYearTagId}&limit=1000').json()
	print(res)
	if res['total'] > res['limit']: print('todo: implement paging')
	entries += res['items']

print(entries)

unPublishPayload = []

for entry in entries:
	unPublishPayload.append({
		'sys': {
			'id': entry['sys']['id'],
			'type': 'Link',
			'linkType': 'Entry'
		}
	})

contentful.bulkAction(unPublishPayload, 'unpublish')

for entry in entries:
	id = entry['sys']['id']
	version = entry['sys']['version']

	res = contentful.session.put(f'https://api.contentful.com/spaces/{contentful.spaceId}/environments/{contentful.environmentId}/entries/{id}/archived', headers={
		'X-Contentful-Version': str(version)
	})
	print('archived', id, res.status_code)

if webhookPreviousActive:
	contentful.setWebhookActive(contentful.vercelWebhookId, True) # reenable
	requests.get(webhookUrl) # manually trigger