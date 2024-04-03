import psycopg2
from dotenv import load_dotenv
from getpass import getpass
from os import environ
import requests

load_dotenv()
SUPABASE_PG_PASSWORD = environ.get('SUPABASE_PG_PASSWORD') or getpass(
	"Enter Supabase Postgres password: ")

EXCLUDE_EMAILS = ["24cdingwall@gmail.com", "ccreativecnd@gmail.com", "cyfinfaza@gmail.com"]

def query_contentful(query):
    url = 'https://graphql.contentful.com/content/v1/spaces/e34g9w63217k/'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + 'TRlCo1BlTmpwyKIOHJ08X2lYAaNNlceF415KMmKkMFk'
    }

    response = requests.get(url, params={'query': query}, headers=headers)

    if not response.ok:
        raise Exception(response.text)

    return response.json()['data']

club_query = '''
{
	clubCollection(order: name_ASC) {
		items {
			slug
			name
		}
	}
}
'''

def getInterestsEmails():
	conn = psycopg2.connect(database="postgres",
							host="db.gahyqgeshbvyajzukktr.supabase.co",
							user="postgres",
							password=SUPABASE_PG_PASSWORD,
							port="5432")

	cursor = conn.cursor()
	cursor.execute(
		"select interests.interest_slug, auth.users.email, auth.users.raw_user_meta_data from interests inner join auth.users on auth.users.id=interests.owner")
	interestsData = cursor.fetchall()

	#filter out all interests with excluded emails
	interestsData = list(filter(lambda interest: interest[1] not in EXCLUDE_EMAILS, interestsData))

	interestEmailsForEachClub = {}
	for interest in interestsData:
		[clubSlug, email, metadata] = interest
		if clubSlug not in interestEmailsForEachClub:
			interestEmailsForEachClub[clubSlug] = []
		fullName = metadata['full_name']
		interestEmailsForEachClub[clubSlug].append({
			'email': email,
			'fullName': fullName
		})

	clubs = query_contentful(club_query)['clubCollection']['items']

	interestEmails = []
	for clubSlug in interestEmailsForEachClub.keys():
		clubName = list(filter(lambda club: club['slug'] == clubSlug, clubs))[
			0]['name']
		interestEmails.append({
			'clubName': clubName,
			'people': interestEmailsForEachClub[clubSlug]
		})

	return interestEmails


if __name__ == "__main__":
	interestEmails = getInterestsEmails()
	topMessage = "As a part of the interest list feature in the 4-H Fair App, we collect the username and email of every person who adds a club to their interest list so that we can report this data to club leaders. Below is a list of usernames/emails who expressed interest in each club. If a club is not listed, this means that no fair app users added that club to their interest list. Club leaders should consider adding emails from this list to their club's mailing list."
	markdownOutput = f'# 4-H Fair App Interest List Emails Report  \n{topMessage}  \n'
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
	for entry in interestEmails:
		markdownOutput += f"## {entry['clubName']}  \n"
		htmlOutput += f"<h2>{entry['clubName']}</h2><ul>"
		for person in entry['people']:
			markdownOutput += f"- {person['fullName']} <[{person['email']}]({person['email']})>\n"
			htmlOutput += f"<li>{person['fullName']} &lt;<a href='mailto:{person['email']}'>{person['email']}</a>&gt;</li>"
		markdownOutput += '  \n'
		htmlOutput += '</ul>'
		emailsSemicolonSeparated = '; '.join(
			map(lambda person: person['email'], entry['people']))
		if len(entry['people']) > 1:
			markdownOutput += f"Quick copy paste: {emailsSemicolonSeparated}  \n"
			htmlOutput += f"<p>Quick copy paste: {emailsSemicolonSeparated}</p>"
	htmlOutput += '</body></html>'
	print(markdownOutput)
	import tempfile
	import webbrowser
	with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as f:
		url = 'file://' + f.name
		f.write(htmlOutput.encode('utf-8'))
	webbrowser.open(url)
