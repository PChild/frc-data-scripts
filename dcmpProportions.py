import gen
import eventTypes
from tqdm import tqdm

tba = gen.setup()
currentYear = 2019

keyBases = [' Dist Teams', ' DCMP Teams', ' % DCMP']

distKeys = []
for year in range(2009, currentYear + 1):
    for district in tba.districts(year):
        dist = district['key']
        distAb = dist[4:].upper()
        
        if distAb not in distKeys:
            distKeys.append(distAb)

distData = []    
for year in tqdm(range(2009, currentYear + 1)):
    yearData = {'Year': year}
    
    for abbr in distKeys:    
        for base in keyBases:
                yearData[abbr + base] = ''
                
    for district in tba.districts(year):       
        distCode = district['key']
        distTeams = len(tba.district_teams(distCode, False, True))
        
        distName = distCode[4:].upper()
        yearData[distName + ' Dist Teams'] =  distTeams
        
        dcmpTeams = []

        for event in tba.district_events(distCode):
            if event['event_type'] in [eventTypes.DISTRICT_CMP_DIVISION, eventTypes.DISTRICT_CMP]:
                dcmpTeams += tba.event_teams(event['key'], False, True)
                
        dcmpTeams = len(list(set(dcmpTeams)))
        yearData[distName + ' DCMP Teams'] = dcmpTeams
        
        yearData[distName + ' % DCMP'] = round(dcmpTeams / distTeams * 100, 2)
        
    distData.append(yearData)

columns = ['Year']
for dist in distKeys:
    for base in keyBases:
        columns.append(dist + base)
        
gen.listOfDictToCSV('DCMP Proportions Data', distData, columns)