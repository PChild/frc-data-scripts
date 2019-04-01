import gen
from tqdm import tqdm

tba = gen.setup()

currentWeek = 5
year = 2019
dist = 'fnc'

sandstormPts = 12
climbPts = 36
totalPts = sandstormPts + climbPts

climbWins = []

for event in tqdm(tba.district_events(str(year) + dist)):
    if event['week'] < currentWeek - 1:
        eventData = {'Event': event['key'], 'Quals Wins': 0, 'Quals Matches': 0, 'Elims Wins': 0, 'Elims Matches': 0, 'Total Wins': 0, 'Total Matches': 0}
        
        for match in tba.event_matches(event['key']):
            eventData['Total Matches'] += 1
            
            if match['comp_level'] == 'qm':
                eventData['Quals Matches'] += 1
            else:
                eventData['Elims Matches'] += 1
                
            if match['alliances']['red']['score'] < totalPts or match['alliances']['blue']['score'] < totalPts:
                if match['comp_level'] == 'qm':
                    eventData['Quals Wins'] += 1
                else:
                    eventData['Elims Wins'] += 1
        eventData['Total Wins'] = eventData['Quals Wins'] + eventData['Elims Wins']
        eventData['Quals Win %'] = round(eventData['Quals Wins'] / eventData['Quals Matches'] , 3)
        eventData['Elims Win %'] = round(eventData['Elims Wins'] / eventData['Elims Matches'] , 3)
        eventData['Total Win %'] = round(eventData['Total Wins'] / eventData['Total Matches'] , 3)
        climbWins.append(eventData)

climbWins = sorted(climbWins, key= lambda event: event['Total Win %'], reverse=True)

outCols = ['Event']
for prefix in ['Quals', 'Elims', 'Total']:
    for suffix in [' Wins', ' Matches', ' Win %']:
        outCols.append(prefix + suffix)
        
gen.listOfDictToCSV(dist.upper() + ' Climbing Wins', climbWins, outCols)