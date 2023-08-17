# converted by ChatGPT from src/logic/contentful.js

import requests

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

clubs = []
club_query = '''
{
    clubCollection(order: name_ASC) {
        items {
            slug
            name
            meetingLocation
            clubWebsite
            description
            grades
            meetingWhen
            listingWebsite
            tent
        }
    }
}
'''

def get_clubs():
    global clubs
    if not clubs:
        clubs = query_contentful(club_query)['clubCollection']['items']
    return clubs

sponsors = []
sponsor_query = '''
{
    sponsorSpotCollection {
        items {
            heading
            image {
                url
            }
            description
            link
            tier
        }
    }
}
'''

def get_sponsors():
    global sponsors
    if not sponsors:
        sponsors = query_contentful(sponsor_query)['sponsorSpotCollection']['items']
    return sponsors
