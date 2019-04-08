import gen
import eventTypes
import slffFunctions
import statistics as stat
from tqdm import tqdm

tba = gen.setup()

dist = 'in'
year = 2019

cmpTypes = [eventTypes.PRESEASON, eventTypes.DISTRICT_CMP, eventTypes.DISTRICT_CMP_DIVISION, eventTypes.CMP_DIVISION, eventTypes.CMP_FINALS]

print('Fetching district events')
distEvents = tba.district_events(str(year) + dist)
dcmpEvents = [event for event in distEvents if event['event_type'] in cmpTypes]

print('Fetching DCMP / divisions teams')
dcmpTeams = []
for event in dcmpEvents:
    dcmpTeams += tba.event_teams(event['key'], False, True)

dcmpTeams = list(set(dcmpTeams))
dcmpTeams = ['frc118', 'frc148', 'frc231', 'frc418', 'frc624', 'frc1255', 'frc1296',
             'frc1477', 'frc1817', 'frc2158', 'frc2468', 'frc2582', 'frc2613',
             'frc2657', 'frc2714', 'frc2881', 'frc3005', 'frc3035', 'frc3240',
             'frc3310', 'frc3481', 'frc3676', 'frc3679', 'frc3735', 'frc3834',
             'frc3847', 'frc4063', 'frc4153', 'frc4192', 'frc4206', 'frc4295',
             'frc4378', 'frc4587', 'frc4610', 'frc5052', 'frc5242', 'frc5261',
             'frc5411', 'frc5414', 'frc5417', 'frc5427', 'frc5431', 'frc5572',
             'frc5866', 'frc5892', 'frc6144', 'frc6315', 'frc6321', 'frc6377',
             'frc6672', 'frc6800', 'frc6901', 'frc6974', 'frc7088', 'frc7121',
             'frc7179', 'frc7271', 'frc7312', 'frc7492', 'frc7494', 'frc7521',
             'frc7621', 'frc7708', 'frc7872']

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