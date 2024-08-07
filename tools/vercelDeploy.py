import contentful
import requests

url = f'https://api.contentful.com/spaces/{contentful.spaceId}/webhook_definitions/{contentful.vercelWebhookId}'

get = contentful.session.get(url)
if get.status_code != 200:
	raise Exception(f'failed to get webhook {contentful.vercelWebhookId}: {get.json()}')

data = get.json()

deploy = requests.get(data['url']) # manually trigger
print(deploy.status_code, deploy.text)