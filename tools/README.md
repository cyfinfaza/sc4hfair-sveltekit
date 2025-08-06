this scripts are not yet migrated to the new [admin panel](https://github.com/caburum/sc4hfair-admin)

## tent setup (required first)

1. ensure `/src/data/tentSlugs.json` matches the source of truth
2. `python tentsToContentfulSchema.py`

## mapbox

1. `python addTentNamesToGeoJSON.py` or todo: mapbox api version

## clubs

1. `pip install -r requirements.txt`
2. check any overrides in `updateClubData.py`
3. `python updateClubData.py`
4. check changes to `clubData.json`, look for missing tents
5. update mapping in `tentsToClubs.json`, make sure all clubs are accounted for
6. `python updateClubData.py` again (optional, or make the changed from 5 as you go)
7. `python clubDataToContentful.py`
8. if adding later, use `python updateContentfulClubTents.py` to only push tent changes

## sponsors

1. `python sponsorsToContentful.py`
2. manually update images in contentful

## scavenger hunt

1. update [spreadsheet](https://docs.google.com/spreadsheets/d/1bZOR5OJGdfSsDHBrOQ8M8MLmdpF-C8HQhxqs43qVWMo/edit)
2. `python createScavengerHuntClues.py`

## interests

1. `python getInterestsEmails.py`

## deprecated

- `newYear.py`
- `archiveLastYearContentful.py`
- `foodVendorsToContentful.py`
- `scheduleToContentful.py`
