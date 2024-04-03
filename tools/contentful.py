import dotenv
from os import environ
import requests
import sys
from time import sleep

dotenv.load_dotenv()

spaceId = 'e34g9w63217k'
environmentId = 'master'
cmaToken = environ.get('CONTENTFUL_CMA_TOKEN')

# update this when starting to import data for a new year
# also ensure tag has been created with name "year: XXXX" and id "XXXX" in the contentful web interface
lastYearTagId = '2023'
yearTagId = '2024'

session = requests.Session()
session.headers.update({
	'Authorization': 'Bearer ' + cmaToken,
	'Content-Type': 'application/vnd.contentful.management.v1+json',
})

noPublish = '--no-publish' in sys.argv

vercelWebhookId = '2pNxUMPQKUMQz2aIHSO65Y'

def setWebhookActive(webhookId, active) -> tuple[bool, str]:
	"""
	return: previous webhook active state, webhook url
	"""

	url = f'https://api.contentful.com/spaces/{spaceId}/webhook_definitions/{webhookId}'

	get = session.get(url)
	if get.status_code != 200:
		raise Exception(f'failed to get webhook {webhookId}: {get.json()}')

	data = get.json()

	previousActive = data['active']

	data['active'] = active

	version = data['sys']['version']
	del data['sys']

	put = session.put(url, json=data, headers={
		'X-Contentful-Version': str(version),
	})
	if put.status_code != 200:
		raise Exception(f'failed to put webhook {webhookId}: {put.json()}')
	
	return (previousActive, data['url'])

def conditionalBulkPublish(publishPayload):
	"""
	publish entries in bulk if there are any, including noPublish & webhook safety
	"""

	if noPublish or len(publishPayload) == 0: return

	(webhookPreviousActive, webhookUrl) = setWebhookActive(vercelWebhookId, False)

	bulkReq = session.post(f'https://api.contentful.com/spaces/{spaceId}/environments/{environmentId}/bulk_actions/publish', json={
		'entities': {
			'items': publishPayload,
		},
	})

	print('bulk publish status', bulkReq.status_code, bulkReq.json()['sys']['status'], bulkReq.json())

	# wait for bulk publish to finish
	while True:
		sleep(5)
		statusReq = session.get(f'https://api.contentful.com/spaces/{spaceId}/environments/{environmentId}/bulk_actions/actions/{bulkReq.json()["sys"]["id"]}')
		status = statusReq.json()['sys']['status']
		print('waiting on bulk publish, status', status)
		if status == 'succeeded':
			break

	if webhookPreviousActive:
		setWebhookActive(vercelWebhookId, True) # reenable
		requests.get(webhookUrl) # manually trigger