"""

Fetches the list of clubs and their details from the 4-H website

python updateClubData.py

"""

import json
import sys
import requests
import bs4
import re
from time import sleep

# some data on the 4h website is outdated
# make sure to also add permanent changes here as the script will overwrite the data if its only changed in contentful
clubDataOverrides = {
	'computer-club': {
		"slug": "4h-computers",
		"name": "4-H Computers",
		"description": "From microcontrollers to gaming PCs and from Scratch to full-stack web apps, 4-H Computers is a club for students who have a passion for electronics and software. We work together to help each other complete projects and build friendships along the way. Our club's work culminates in the 4-H Fair in August, where we get to show off all of our projects to the public. We are also responsible for developing and maintaining the 4-H Fair App, a project started several years ago that our club adopted in 2020. While anyone is welcome to join our club, our club is not a class, and we are more geared towards self-driven individuals who already have an interest in electronics and software.",
		"meeting_where": "Ted Blum 4-H Center or Discord virtual call",
		"meeting_when": "Every first and third Friday from 7pm to 9pm",
		"grades": "Mainly 7-12",
		"clubWebsite": "https://4hcomputers.club"
	}
}

tentsToClubs = json.load(open('tentsToClubs.json'))
clubsToTents = {}
for tent in tentsToClubs:
	for club in tentsToClubs[tent]:
		clubsToTents[club] = tent

clubData = []
doneSlugs = [] # because of course some listings are duplicated

for clubListing in ['https://4histops.org/clubs', 'https://4histops.org/4-h-prep-club']:
	content = requests.get(clubListing).content.decode('utf-8')

	# fix some issues with the 4h site
	content = re.sub(r'\/technomaniacs(?=\">WATTLES)', '/wattles-snood', content)
	content = re.sub(r'\/technomaniacs(?=\">WOOLLY)', '/woolly-ones', content)

	soup = bs4.BeautifulSoup(content, 'html.parser')

	# navigate to each club
	for club in soup.select('ul h3 a'):
		while True:
			slug = club.get('href').strip()
			if slug.startswith('http'): slug = slug[len('https://4histops.org/'):]
			if slug.startswith('/'): slug = slug[1:]

			if slug in doneSlugs:
				print('duplicate slug detected:', slug)
				break
			print('scraping', slug)

			listingWebsite = 'https://4histops.org/' + slug
			page = requests.get(listingWebsite)
			soup = bs4.BeautifulSoup(page.content, 'html.parser')
			block = soup.select_one('.sqs-layout')

			if page.status_code == 429:
				print('ratelimited')
				sleep(10)
				continue # retry this club
			elif page.status_code != 200:
				print('error:', page.status_code)
				break

			try:
				data = {
					'listingWebsite': listingWebsite,
					'slug': slug,
					'name': block.find('h2').text.title().replace('And', 'and').strip(), # it's transformed to upper case so the actual value is random cases
					'description': block.find('p').text.strip(),
					'meetingLocation': '',
					'meetingWhen': '',
					'grades': '',
				}

				for field in block.find_all('p'):
					value = field.text.strip().split(':')
					key = value.pop(0).lower()
					value = ':'.join(value).strip()

					if key == 'where': data['meetingLocation'] = value
					elif key == 'when': data['meetingWhen'] = value
					elif key == 'grades':
						short = re.search(r'^(K|\d{1,2})\s?-\s?(\d{1,2})$', value) # formats things like "K - 12" or "1 -3"
						if short != None: value = short.group(1) + '-' + short.group(2)
						data['grades'] = value

				if slug in clubDataOverrides:
					data.update(clubDataOverrides[slug])

				if slug in clubsToTents:
					data['tent'] = clubsToTents[slug]

				doneSlugs.append(slug)
				clubData.append(data)

			except AttributeError as e: # couldn't find one of the items
				print(e)
				print('---')
				print(page.status_code)
				print('---')
				print(block)
				print('---')
				print(soup.select_one('.Main-content'))
				continue

			sleep(1)
			break # exit this infinite loop and go to the next club

with open('clubData.json', 'w') as file:
	json.dump(clubData, file, indent='\t')
	file.close()