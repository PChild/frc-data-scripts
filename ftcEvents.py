import gen
import requests
import geocoder
from pathlib import Path
import csv
import re
from time import sleep

zipPattern = re.compile("\d+\-\d+")
fileName = "ftcData.csv"
ftcData = []

def handleZip(obj):
    zipCode = ""
    try: 
        location = geocoder.osm(obj['city'] + ", " + obj['state_prov'] + " " + obj['country'])
        if not location.postal:
            location = geocoder.osm((location.lat, location.lng), method="reverse")
        sleep(1)
        zipCode = location.postal
        if obj['country'] == "Canada":
            zipCode = zipCode[:3]
    except:
        pass
    return zipCode

def fetchFtcData():
    baseUrl = "http://theorangealliance.org/apiv2/"
    headers = {"X-Application-Origin": "PyScout", "X-TOA-Key": "dL5DVJ5oOPth7vtDJmZ1J3MetkNjcZ1PIyN0fgCxiiyx2kh7pEz13A=="}
    teams = requests.get(baseUrl + "teams", headers=headers).json()
    events = requests.get(baseUrl + "events", headers=headers).json() 
    return [teams, events]

def find(lst, key, value):
    for (i, dic) in enumerate(lst):
        if dic[key] == value:
            return i
    return -1

#If possible load in already collected data to save time.
if Path(fileName).exists():
    print("Loading data from file")
    fileData = csv.DictReader(open(fileName), skipinitialspace=True)
    for row in fileData:
        ftcData.append(row)
#Fetch and add data if there wasn't any saved data already.
else:
    print("No data file found, generating.")
    badTeams = 0
    badEvents = 0
    [teams, events] = fetchFtcData()
    for (idx, team) in enumerate(teams):
        gen.progressBar(idx, len(teams))
        zipCode = handleZip(team)
        if zipCode == "":
            badTeams += 1
        ftcData.append({"type": "Team", "location": zipCode, "country": team['country'], "key": "ftc" + str(team['team_number'])})
    for (idx, event) in enumerate(events):
        gen.progressBar(idx, len(events))
        zipCode = handleZip(team)
        if zipCode == "":
            badEvents += 1
        ftcData.append({"type": "Event", "location": zipCode, "country": event['country'], "key": event['event_key']})
    print("\n", badTeams, "out of", len(teams), "teams were bad.")
    print(badEvents, "out of", len(events), "events were bad.")




modifiedCount = 0
[teams, events] = fetchFtcData()

for (idx, obj) in enumerate(ftcData):
    gen.progressBar(idx, len(ftcData))
    item = ""
    
    if obj['type'] == "Team":
        item = teams[find(teams, 'team_number', obj['key'][3:])]
    else:
        item = events[find(events, 'event_key', obj['key'])]
    
    if obj['location'] == 'None' or obj['location'] == None or obj['location'] == '':
        obj['location'] = handleZip(item)
        modifiedCount += 1
    
    if bool(zipPattern.match(obj['location'])):
        obj['location'] = obj['location'][:5]
        modifiedCount += 1
    if(len(obj['location']) == 4 and obj['country'] == 'USA'):
        obj['location'] = str(0) + obj['location']
        modifiedCount += 1
    if (obj['location'][:3] == "AK " ):
        obj['location'] = obj['location'][3:][:5]
        modifiedCount += 1
        
    
print("Updated", modifiedCount, "objects out of", len(ftcData))
gen.listOfDictToCSV("ftcData", ftcData)