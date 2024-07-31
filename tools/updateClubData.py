"""

Fetches the list of clubs and their details from the 4-H website

python updateClubData.py

"""

import json
import traceback
import requests
import bs4
import re
from time import sleep

# some data on the 4h website is outdated
# make sure to also add permanent changes here as the script will overwrite the data if its only changed in contentful
clubDataOverrides = {
	'computer-club': {
		"slug": "4h-computers",
		"name": "4‑H Computers",
		"grades": "Mainly 7-12",
		"clubWebsite": "https://4hcomputers.club"
	},
	'prep-lego-maniacs': {
		"grades": "K-3",
	}
}

tentsToClubs = json.load(open('tentsToClubs.json'))
clubsToTents = {}
for tent in tentsToClubs:
	for club in tentsToClubs[tent]:
		clubsToTents[club] = tent

def cleanString(str):
	return str.strip().replace('4-H', '4‑H')

clubData = []
doneSlugs = [] # because of course some listings are duplicated

def cleanTag(tag: bs4.element.Tag, inParentheses=False):
	text = tag.text.lower()
	if inParentheses: text = text.split('(')[1].split(')')[0]
	return text.strip().replace(' and ', ' & ').replace(chr(174), '').split(', ')

for clubListing in ['https://4histops.org/clubs', 'https://4histops.org/4-h-prep-club']:
	content = requests.get(clubListing).content.decode('utf-8')

	# fix some issues with the 4h site
	content = re.sub(r'\/technomaniacs(?=\">WATTLES)', '/wattles-snood', content)

	soup = bs4.BeautifulSoup(content, 'html.parser')

	# navigate to each club
	for h3 in soup.select('ul h3'):
		# <h3 style="white-space:pre-wrap;"><a href="https://4histops.org/4h-beekeeping-club">4-H Beekeeping Club</a> (Beekeeping)</h3>
		club = h3.find('a')

		if not club: continue

		tags = []

		# tag is previous header
		try:
			tags.extend(cleanTag(h3.find_parent('div', class_='row sqs-row').find_previous_sibling('div', class_='row sqs-row').find('h1')))
		except AttributeError:
			pass
		try:
			tags.extend(cleanTag(h3.find_parent('div', class_='row sqs-row').find_previous_sibling('div', class_='sqs-block html-block sqs-block-html').find('h1')))
		except AttributeError:
			pass

		# tag in parentheses
		try:
			tags.extend(cleanTag(h3, True))
		except AttributeError:
			pass

		tags = list(dict.fromkeys(tags)) # remove duplicates

		slug = club.get('href').strip()
		if slug.startswith('https://4histops.org/'): slug = slug[len('https://4histops.org/'):]
		if slug.startswith('https://'): slug = slug[len('https://'):] # broken link (https://puppet-club)
		if slug.startswith('/'): slug = slug[1:]

		if slug == '':
			print('empty slug detected:', club)
			break

		if slug in doneSlugs:
			print('duplicate slug detected:', slug)
			break

		while True:
			print('scraping', slug)
			listingWebsite = 'https://4histops.org/' + slug
			page = requests.get(listingWebsite)
			soup = bs4.BeautifulSoup(page.content, 'html.parser')
			block = soup.select_one('.sqs-layout')

			if page.status_code == 429 or page.status_code >= 500:
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
					'tags': tags,
					'name': cleanString(block.find('h2').text.title().replace('And', 'and').replace('(Prep)', '(PREP)')), # it's transformed to upper case so the actual value is random cases
					'description': '',
					'meetingLocation': '',
					'meetingWhen': '',
					'grades': '',
				}

				for field in block.find_all('p'):
					text = field.text.strip()
					value = text.split(':')
					key = value.pop(0).lower()
					value = cleanString(':'.join(value).strip())

					if key == 'where': data['meetingLocation'] = value
					elif key == 'when': data['meetingWhen'] = value
					elif key == 'grades':
						short = re.search(r'^(K|\d{1,2})\s?-\s?(\d{1,2})$', value) # formats things like "K - 12" or "1 -3"
						if short is not None: value = short.group(1) + '-' + short.group(2)
						data['grades'] = value
					elif key == 'description':
						pass # broken 4h website thing
					elif 'not accepting new members' not in text.lower():
						# another part of the description probably, but ignore not accepting new members as the fair/next year is later
						data['description'] = data['description'] + '\n\n' + text

				data['description'] = data['description'].strip()

				if slug in clubDataOverrides:
					data.update(clubDataOverrides[slug])

				if data['slug'] in clubsToTents:
					data['tent'] = clubsToTents[data['slug']]

				doneSlugs.append(slug)
				clubData.append(data)

			except AttributeError as e: # couldn't find one of the items
				print(e)
				traceback.print_exception(e)
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

print('\nclub data updated, run `python clubDataToContentful.py` to publish')