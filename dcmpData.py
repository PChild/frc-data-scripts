import gen
import eventTypes
import slffFunctions
import statistics as stat
from tqdm import tqdm

tba = gen.setup()

dist = 'ont'
year = 2019

cmpTypes = [eventTypes.DISTRICT_CMP, eventTypes.DISTRICT_CMP_DIVISION]
ignoreEvents = cmpTypes + [eventTypes.CMP_DIVISION, eventTypes.CMP_FINALS, eventTypes.PRESEASON]

print('Fetching district events')
distEvents = tba.district_events(str(year) + dist)
dcmpEvents = [event for event in distEvents if event['event_type'] in cmpTypes]

print('Fetching DCMP / divisions teams')
dcmpTeams = []
for event in dcmpEvents:
    dcmpTeams += tba.event_teams(event['key'], False, True)

dcmpTeams = list(set(dcmpTeams))
dcmpTeams = ['frc188', 'frc610', 'frc746', 'frc771', 'frc772', 'frc854', 
             'frc865', 'frc907', 'frc1075', 'frc1114', 'frc1241', 'frc1285', 
             'frc1305', 'frc1310', 'frc1325', 'frc1360', 'frc2056', 'frc2200', 
             'frc2386', 'frc2634', 'frc2702', 'frc2706', 'frc2852', 'frc2994', 
             'frc3683', 'frc3739', 'frc4039', 'frc4069', 'frc4152', 'frc4343', 
             'frc4476', 'frc4519', 'frc4525', 'frc4618', 'frc4678', 'frc4688', 
             'frc4783', 'frc4814', 'frc4903', 'frc4907', 'frc4914', 'frc4917', 
             'frc4920', 'frc4932', 'frc4936', 'frc4939', 'frc4946', 'frc4976', 
             'frc4992', 'frc5024', 'frc5036', 'frc5406', 'frc5409', 'frc5483', 
             'frc5672', 'frc5719', 'frc5834', 'frc5885', 'frc6070', 'frc6135', 
             'frc6140', 'frc6141', 'frc6336', 'frc6378', 'frc6461', 'frc6867', 
             'frc6878', 'frc6987', 'frc7022', 'frc7136', 'frc7476', 'frc7480', 
             'frc7520', 'frc7558', 'frc7664', 'frc7722']

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
        if event['event_type'] not in ignoreEvents:
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