import gen
import geocoder
from geoDicts import states, provs


tba = gen.setup()

YEAR = 2018

data = []
usedStates = []

inDistricts = ['MI', 'IN', 'VA', 'MD', 'DC', 'NC', 'GA', 'RI', 'MA', 'ME', 'VT', 'WA', 'OR', 'DE', 'PA', 'NH', 'NJ', 'ON', 'TX', 'CT']

newNames = []
for abbrv in inDistricts:
    try:
        newNames.append(states[abbrv])
    except:
        newNames.append(provs[abbrv])
inDistricts.append("Israel")
inDistricts.append("ISR")
inDistricts += newNames

def handleZip(teamOrEvent):
    try:
        if teamOrEvent['postal_code'] == None:
            tmpLoc = geocoder.osm(teamOrEvent['city'] + ", " + teamOrEvent['state_prov'] + " " + teamOrEvent['country'])
            zipCode = geocoder.osm((tmpLoc.lat, tmpLoc.lng), method="reverse").postal
        else:
            zipCode = teamOrEvent['postal_code']
        
        if teamOrEvent['country'] == "Canada":
            zipCode = zipCode[:3]
    except:
        zipCode = ""
    return zipCode

seasonEvents = tba.events(2018)
for (idx, event) in enumerate(seasonEvents):
    gen.progressBar(idx, len(seasonEvents))
    district = False
    
    if event['district'] != None:
        district = True
    
    if event['state_prov'] == "TX" or event['state_prov'] == 'PA':
        district = True
    
    if event['event_type'] in range(0,6):
        data.append({"type": "Event", 
                     "key": event['key'], 
                     "zip": handleZip(event), 
                     "state": event['state_prov'], 
                     "country": event['country'], 
                     "district": district })
        
        if event['state_prov'] not in usedStates:
            usedStates.append(event['state_prov'])

for state in states:
    if state not in usedStates:
        isDist = False
        
        if state in inDistricts:
            isDist = True
        data.append({"type": "Event", 
                     "key": "", 
                     "zip": "", 
                     "state": state, 
                     "country": "US", 
                     "district": isDist })

for prov in provs:
    if prov not in usedStates:
        isDist = False
        
        if prov in inDistricts:
            isDist = True    
        data.append({"type": "Event",
                     "key": "", 
                     "zip": "", 
                     "state": prov, 
                     "country": "Canada", 
                     "district": isDist })  


teams = []

for page in range(0,20):
    gen.progressBar(page, 20)
    for team in tba.teams(page, YEAR):
        data.append({"type": "Team",
                     "key": team['key'], 
                     "zip": handleZip(team), 
                     "state": team['state_prov'], 
                     "country": team['country'], 
                     "district": (team['country'] in inDistricts or team['state_prov'] in inDistricts) })  
        
colOrder = ["key", "type", "zip", "state", "country", "district"]
gen.listOfDictToCSV(str(YEAR) + "eventLocations", data, colOrder)