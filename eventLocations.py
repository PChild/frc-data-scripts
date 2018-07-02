import gen
from geoDicts import states, provs


tba = gen.setup()

YEAR = 2018

events = []
usedStates = []

inDistricts = ['MI', 'IN', 'VA', 'MD', 'DC', 'NC', 'GA', 'RI', 'MA', 'ME', 'VT', 'WA', 'OR', 'DE', 'PA', 'NH', 'NJ', 'ON', 'TX']

seasonEvents = tba.events(2018)
for (idx, event) in enumerate(seasonEvents):
    gen.progressBar(idx, len(seasonEvents))
    district = False
    
    if event['district'] != None:
        district = True
    
    if event['state_prov'] == "TX" or event['state_prov'] == 'PA':
        district = True
    
    if event['event_type'] in [0,1]:
        zipCode = event['postal_code']
        if event['country'] == "Canada":
            zipCode = zipCode[:3]
        events.append({"key": event['key'], "zip": zipCode, "state": event['state_prov'], "country": event['country'], "district": district})
        
        if event['state_prov'] not in usedStates:
            usedStates.append(event['state_prov'])

for state in states:
    if state not in usedStates:
        isDist = False
        
        if state in inDistricts:
            isDist = True
        events.append({"key": "", "zip": "", "state": state, "country": "US", "district": isDist})

for prov in provs:
    if prov not in usedStates:
        isDist = False
        
        if prov in inDistricts:
            isDist = True    
        events.append({"key": "", "zip": "", "state": prov, "country": "Canada", "district": isDist})  

colOrder = ["key", "zip", "state", "country", "district"]
gen.listOfDictToCSV(str(YEAR) + "eventLocations", events, colOrder)