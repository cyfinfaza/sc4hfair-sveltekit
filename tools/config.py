import dotenv
from os import environ
import requests
import sys

dotenv.load_dotenv()

spaceId = 'e34g9w63217k'
environmentId = 'master'
cmaToken = environ.get('CONTENTFUL_CMA_TOKEN')

session = requests.Session()
session.headers.update({
	'Authorization': 'Bearer ' + cmaToken,
	'Content-Type': 'application/vnd.contentful.management.v1+json',
})

noPublish = '--no-publish' in sys.argv