import dotenv
from os import environ

dotenv.load_dotenv()

spaceId = 'e34g9w63217k'
environmentId = 'master'
cmaToken = environ.get('CONTENTFUL_CMA_TOKEN')