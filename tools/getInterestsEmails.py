from contentful import currentYear
from dotenv import load_dotenv
from os import environ
from pymongo import MongoClient
import requests
import tempfile
import webbrowser

INCLUDE_DEVS = True

load_dotenv()

mongo = MongoClient(environ.get('MONGODB_SECRET'))
db = mongo.interests
interests = db.interests

def query_contentful(query):
	url = 'https://graphql.contentful.com/content/v1/spaces/e34g9w63217k/'
	headers = {
		'Content-Type': 'application/json',
		'Authorization': 'Bearer ' + 'TRlCo1BlTmpwyKIOHJ08X2lYAaNNlceF415KMmKkMFk'
	}

	response = requests.get(url, params={'query': query}, headers=headers)

	if not response.ok: raise Exception(response.text)

	return response.json()['data']

club_query = '''{
	clubCollection(order: name_ASC) {
		items {
			slug
			name
		}
	}
}'''
clubs = query_contentful(club_query)['clubCollection']['items']
slugToName = {club['slug']: club['name'] for club in clubs}

data = interests.aggregate([
	{
		# Stage 1: Filter interests by year.
		'$match': {
			'year': currentYear 
		}
	},
	{
		# Stage 2: Perform a left outer join to the users collection.
		'$lookup': {
			'from': 'users',
			'localField': 'user_id',
			'foreignField': '_id',
			'as': 'userDetails'
		}
	},
	{
		# Stage 3: Deconstruct the userDetails array to process each joined document.
		'$unwind': '$userDetails'
	},
	{
		# Stage 4: Filter out documents where the user's role is 'dev'.
		'$match': {} if INCLUDE_DEVS else {
			'userDetails.role': { '$ne': 'dev' }
		}
	},
	{
		# Stage 5: Group the remaining documents by interest slug.
		'$group': {
			'_id': '$slug',
			'users': {
				# Push the relevant user details into a 'users' array.
				'$push': {
					'email': '$userDetails.email',
					'name': '$userDetails.name'
				}
			}
		}
	},
	{
		# Stage 6: Sort the results alphabetically by the interest slug (_id).
		'$sort': { '_id': 1 } # 1 for ascending order
	},
	{
		# Stage 7: Reshape the output documents for final presentation.
		'$project': {
			'_id': 1,
			'users': 1
		}
	}
])

topMessage = "As a part of the interest list feature in the 4-H Fair App, we collect the name and email of every person who adds a club to their interest list so that we can report this data to club leaders. Below is a list of names/emails who expressed interest in each club. If a club is not listed, this means that no fair app users added that club to their interest list. Club leaders should consider adding emails from this list to their club's mailing list. You can copy and paste each section directly into an email recipients box."

markdownOutput = f'# 4-H Fair App Interest List Emails Report\n{topMessage}'
htmlOutput = f"""<html>
<head>
	<title>4-H Fair App Interest List Emails Report</title>
	<style>
		body {{
			font-family: sans-serif;
		}}
		h2 {{
			break-after: avoid;
		}}
	</style>
</head>
<body>
<h1>4-H Fair App Interest List Emails Report</h1>
<p>{topMessage}</p>
"""

for club in data:
	name = slugToName[club['_id']]
	markdownOutput += f"\n\n## {name}"
	htmlOutput += f"<h2>{name}</h2><ul>"

	for user in club['users']:
		markdownOutput += f"\n- {user['name']} <[{user['email']}]({user['email']})>"
		htmlOutput += f"<li>{user['name']} &lt;<a href='mailto:{user['email']}'>{user['email']}</a>&gt;</li>"

	htmlOutput += '</ul>'

htmlOutput += '</body></html>'

print(markdownOutput)

with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as f:
	url = 'file://' + f.name
	f.write(htmlOutput.encode('utf-8'))
webbrowser.open(url)

mongo.close()