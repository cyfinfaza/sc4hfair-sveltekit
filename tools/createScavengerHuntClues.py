"""

Generate clues JSON file from the scavenger hunt Google Sheet:

python3 ./createScavengerHuntClues.py 1bZOR5OJGdfSsDHBrOQ8M8MLmdpF-C8HQhxqs43qVWMo

"""

import requests
import json
import sys
import csv
from datetime import datetime

sheetId = sys.argv[1] if len(sys.argv) > 1 else input("Sheet ID: ")

print("Fetching sheet data...")
response = requests.get(f"https://docs.google.com/spreadsheets/d/{sheetId}/export?format=csv")

rows = csv.reader(response.text.splitlines(), delimiter=',', quotechar='"')

clues = []
falseCodes = []

for row in rows:
	[appInclude, generatorInclude, hung, clue, hint, tent, moreSpecificLocation, code, descriptor] = row[:10]
	if hung == "TRUE" and appInclude == "FALSE":
		falseCodes.append(code)
	elif appInclude == "TRUE":
		clues.append({
			"code": code,
			"clue": clue,
			"hint": hint,
		})

output = json.dumps({"year": datetime.now().year, "clues": clues, "falseCodes": falseCodes}, indent='\t')

with open("../src/data/shClues.json", "w") as f:
	f.write(output)
