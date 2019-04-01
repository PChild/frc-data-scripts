import gen
import eventTypes
import slffFunctions
import statistics as stat
from tqdm import tqdm

tba = gen.setup()

dist = 'isr'
year = 2019

cmpTypes = [eventTypes.DISTRICT_CMP, eventTypes.DISTRICT_CMP_DIVISION, eventTypes.CMP_DIVISION, eventTypes.CMP_FINALS]

print('Fetching district events')
distEvents = tba.district_events(str(year) + dist)
dcmpEvents = [event for event in distEvents if event['event_type'] in cmpTypes]

print('Fetching DCMP / divisions teams')
dcmpTeams = []
for event in dcmpEvents:
    dcmpTeams += tba.event_teams(event['key'], False, True)

dcmpTeams = list(set(dcmpTeams))

print('Processing team performances')
dcmpData = []
for team in tqdm(dcmpTeams):
    teamEvents = tba.team_events(team, year)
    
    teamData = slffFunctions.getPerformanceData(team, year)
    teamData['total'] = []
    teamData['playPts'] = []
    teamData['awardPts'] = []
    teamData['awardStrings'] = []
    teamData['ranks'] = []
    
    for event in teamEvents:
        if event['event_type'] not in cmpTypes:
            playPts = slffFunctions.getPlayPoints(team, event['key'])
            awardPts = slffFunctions.getAwardPoints(team, event['key'])

            teamData['playPts'].append(sum(playPts[0:3]))
            teamData['ranks'].append(playPts[3])
            teamData['total'].append(sum(playPts[0:2]) + awardPts[0])
            teamData['awardPts'].append(awardPts[0])
            teamData['awardStrings'].append(awardPts[1])
    
    dcmpData.append(teamData)

finalData = []
for entry in dcmpData:
    finalDataEntry = {'Team': entry['Team'], 
                    'Max OPR': entry['Max OPR'], 
                    'Avg OPR': entry['Avg OPR'], 
                    'Wins': entry['Wins'], 
                    'Losses': entry['Losses'], 
                    'Ties': entry['Ties'], 
                    'Win %': entry['Win %'],
                    'Avg Total Pts': stat.mean(entry['total']),
                    'Max Total Pts': max(entry['total']),
                    'Avg Play Pts': stat.mean(entry['playPts']),
                    'Max Play Pts': max(entry['playPts']),
                    'Avg Rank': stat.mean(entry['ranks']),
                    'Best Rank': min(entry['ranks']),
                    'Avg Award Pts': stat.mean(entry['awardPts']),
                    'Max Award Pts': max(entry['awardPts']),
                    'Awards Won': ' / '.join(entry['awardStrings'])}
    finalData.append(finalDataEntry)
    
cols = ['Team', 'Win %', 'Wins', 'Losses', 'Ties', 'Max OPR', 'Avg OPR', 'Max Total Pts',
        'Avg Total Pts', 'Avg Rank', 'Best Rank', 'Awards Won', 'Max Play Pts', 'Avg Play Pts', 'Max Award Pts', 'Avg Award Pts']
gen.listOfDictToCSV(str(year)+dist + ' DCMP Data', finalData, cols, True)