"""

Generate clues JSON file from the scavenger hunt Google Sheet:

python ./createScavengerHuntClues.py 1bZOR5OJGdfSsDHBrOQ8M8MLmdpF-C8HQhxqs43qVWMo

"""

import requests
import json
import sys
import csv
from contentful import currentYear

sheetId = sys.argv[1] if len(sys.argv) > 1 else input("Sheet ID: ")

print("Fetching sheet data...")
response = requests.get(f"https://docs.google.com/spreadsheets/d/{sheetId}/gviz/tq?tqx=out:csv&sheet={currentYear}")

rows = csv.reader(response.text.splitlines(), delimiter=',', quotechar='"')

clues = []
falseCodes = []
finalInstructions = 'Visit the info tent desk to claim your prize!'

for row in rows:
	[appInclude, generatorInclude, hung, clue, hint, tent, moreSpecificLocation, code, descriptor] = row[:10]
	if code == "FINAL":
		finalInstructions = clue
	if hung == "TRUE" and appInclude == "FALSE":
		falseCodes.append(code)
	elif appInclude == "TRUE":
		clues.append({
			"code": code,
			"clue": clue,
			"hint": hint,
		})

output = json.dumps({"year": currentYear, "clues": clues, "falseCodes": falseCodes, "finalInstructions": finalInstructions}, indent='\t')

with open("../src/data/shClues.json", "w") as f:
	f.write(output)
