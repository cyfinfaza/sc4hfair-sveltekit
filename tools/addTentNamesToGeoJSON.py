"""

Add names to GeoJSON features based on their slug, and verify that all slugs exist in the slug list.

python3 addTentNamesToGeoJSON.py ../src/data/tentSlugs.json

"""

import json
from sys import argv

with open(argv[1] if len(argv) > 1 else input("tent slugs file: ")) as file:
    tentNames = json.load(file)

with open(input("geojson file: ")) as file:
    data = json.load(file)

slugs = []

for feature in data["features"]:
    properties = feature['properties']
    if 'slug' in properties:
        if properties['slug'] in slugs:
            print("\033[91mduplicate slug: \033[1m" + properties['slug'] + "\033[0m")
        slugs.append(properties['slug'])
        if properties['slug'] in tentNames:
            feature['properties']['name'] = tentNames[properties['slug']]
        else:
            print("\033[93mslug not found: \033[1m" + properties['slug'] + "\033[0m")
    else:
        print("\033[91mno slug for feature id: \033[1m" + feature['id'] + "\033[0m")

with open(input("output file: "), 'w') as file:
    json.dump(data, file)
