import gen
import requests
import geocoder
from pathlib import Path
import csv
import re
from time import sleep
from tqdm import tqdm

zipPattern = re.compile("\d+\-\d+")
fileName = "FTC_DelMarVa.csv"
roi = ['VA', 'MD', 'DE']
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
    return str(zipCode)

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
    for team in tqdm(teams):
        if team['state_prov'] in roi:
            zipCode = handleZip(team)
            if zipCode == "":
                badTeams += 1
            ftcData.append({"type": "Team", 
                            "zip": zipCode, 
                            "country": team['country'], 
                            "key": "ftc" + str(team['team_number']), 
                            'city': team['city'], 
                            'state': team['state_prov'], 
                            'country': team['country']})
    for event in tqdm(events):
        if event['state_prov'] in roi:
            zipCode = handleZip(team)
            if zipCode == "":
                badEvents += 1
            ftcData.append({"type": "Event",
                            "zip": zipCode,
                            "country": event['country'],
                            "key": event['event_key'],
                            'city': event['city'], 
                            'state': event['state_prov'], 
                            'country': event['country']})
    print("\n", badTeams, "out of", len(teams), "teams were bad.")
    print(badEvents, "out of", len(events), "events were bad.")

modifiedCount = 0
[teams, events] = fetchFtcData()

for obj in tqdm(ftcData):
    item = ""
    
    if obj['type'] == "Team":
        item = teams[find(teams, 'team_number', obj['key'][3:])]
    else:
        item = events[find(events, 'event_key', obj['key'])]
    
    if obj['zip'] == 'None' or obj['zip'] == None or obj['zip'] == '':
        obj['location'] = handleZip(item)
        modifiedCount += 1
    
    if bool(zipPattern.match(obj['zip'])):
        obj['zip'] = obj['zip'][:5]
        modifiedCount += 1
    if(len(obj['zip']) == 4 and obj['zip'] == 'USA'):
        obj['zip'] = str(0) + obj['zip']
        modifiedCount += 1
    if (obj['zip'][:3] == "AK " ):
        obj['zip'] = obj['zip'][3:][:5]
        modifiedCount += 1
        
    
print("Updated", modifiedCount, "objects out of", len(ftcData))
gen.listOfDictToCSV(fileName, ftcData)