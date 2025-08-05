"""

Add names to GeoJSON features based on their slug, and verify that all slugs exist in the slug list.

python addTentNamesToGeoJSON.py [year]

todo: use https://docs.mapbox.com/api/maps/datasets/#update-a-dataset to modify the dataset in place

"""

from contentful import currentYear
import json
from sys import argv

year = currentYear

if len(argv) > 1:
	year = argv[1]

# make an open function with a default that will prompt the user if not found
def load_json(file_path: str, name: str) -> tuple[str, str]:
	try:
		with open(file_path, 'r') as file:
			return (json.load(file), file_path)
	except FileNotFoundError:
		print(f"File not found: {file_path}")
		new_path = input(f"{name}: ")
		return load_json(new_path, name)

tentNames, _ = load_json("../src/data/tentSlugs.json", "tent slugs file")
data, data_path = load_json(f"Fair Tents {year}.geojson", "geojson file")
output_path = data_path.replace(".geojson", " with names.geojson")

print(f"loading {data_path}")

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

with open(output_path, 'w') as file:
	print(f"writing {output_path}")
	json.dump(data, file)
