import gen
import eventTypes
import slffFunctions
import statistics as stat
from tqdm import tqdm

tba = gen.setup()

div = 'tes'
year = 2019


eventCode = str(year) + div

ignoreEvents = [eventTypes.CMP_DIVISION, eventTypes.CMP_FINALS, eventTypes.PRESEASON]

print('Fetching division teams')
cmpTeams = tba.event_teams(eventCode, False, True)

print('Processing team performances')
cmpData = []
for team in tqdm(cmpTeams):
    teamEvents = tba.team_events(team, year)
    
    teamData = slffFunctions.getPerformanceData(team, year)
    teamData['total'] = []
    teamData['playPts'] = []
    teamData['awardPts'] = []
    teamData['awardStrings'] = []
    teamData['ranks'] = []
    
    for event in teamEvents:
        if event['event_type'] not in ignoreEvents:
            playPts = slffFunctions.getPlayPoints(team, event['key'])
            awardPts = slffFunctions.getAwardPoints(team, event['key'])

            teamData['playPts'].append(sum(playPts[0:3]))
            teamData['ranks'].append(playPts[3])
            teamData['total'].append(sum(playPts[0:2]) + awardPts[0])
            teamData['awardPts'].append(awardPts[0])
            teamData['awardStrings'].append(awardPts[1])
    
    cmpData.append(teamData)

finalData = []
for entry in cmpData:
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
gen.listOfDictToCSV(str(year)+div.upper() + ' Data', finalData, cols, True)