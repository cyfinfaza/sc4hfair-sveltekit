import psycopg2
from dotenv import load_dotenv
from getpass import getpass
from os import environ
from contentful import get_clubs

load_dotenv()
SUPABASE_PG_PASSWORD = environ.get('SUPABASE_PG_PASSWORD') or getpass(
	"Enter Supabase Postgres password: ")


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

	clubs = get_clubs()

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
	markdownOutput = '# 4-H Fair App Interest List Emails Report\n\n'
	htmlOutput = """<html>
	<head>
		<title>4-H Fair App Interest List Emails Report</title>
		<style>
			body {
				font-family: sans-serif;
			}
		</style>
	</head>
	<body>
	<h1>4-H Fair App Interest List Emails Report</h1>
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
