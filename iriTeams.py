import pandas as pd
import statistics as stat
import tbapy

tba = tbapy.TBA('DJRE7IGB1IBTCtvpZfFnn7aZfBWoY9bTIZfQFY7CVBZ8tWeNRX6x0XdISQ63skHv')

YEAR = 2018

baseList = pd.read_csv('iriIN.csv')
teamsList = []
eventData = {}

for teamNum in baseList['teams']:
    print("Processing team " + str(teamNum))
    teamKey = 'frc' + str(teamNum)
    oprs = []
    awardsString = ""
    awardsCount = 0
    madeChamps = False
    team = tba.team(int(teamNum))
    wins = 0
    losses = 0
    ties = 0
    
    for match in tba.team_matches(int(teamNum), None, YEAR, True, False):
        allyColor = 'blue'
        oppoColor = 'red'        
        
        if teamKey in match['alliances']['red']['team_keys']:
            allyColor = 'red'
            oppoColor = 'blue'          
        
        winner = match['winning_alliance']
        
        wins += winner == allyColor
        losses += winner == oppoColor
        ties += len(winner) is 0    
            
    for award in tba.team_awards(int(teamNum), YEAR):
        awardsString += award['event_key'][4:].upper() + " " + award['name'] + " / "
        awardsCount += 1
    
    for event in tba.team_events(int(teamNum), YEAR):
        if event['event_type'] in range(0,10):
            if event['event_type'] in range(3,5):
                madeChamps = True
            try:
                if event['key'] in eventData.keys():
                    oprs.append(eventData[event['key']]['oprs'][team['key']])
                else:
                    print("Storing event " + event['key'])
                    eventData[event['key']]  = tba.event_oprs(event['key'])
                    oprs.append(eventData[event['key']]['oprs'][team['key']])

            except Exception as e:
                print(e)
    if len(oprs) is 0:
        maxOPR = 0
        avgOPR = 0
    else:
        maxOPR = max(oprs)
        avgOPR = stat.mean(oprs)
    teamData = {'num': team['team_number'], 'name': team['nickname'], 'maxOPR': maxOPR, 'avgOPR': avgOPR, 'wins': wins, 'losses': losses, 'ties': ties, 'country': team['country'], 'state': team['state_prov'], 'rookie_year': team['rookie_year'], 'madeChamps': madeChamps, 'awardCount': awardsCount, 'awardsList': awardsString}
    teamsList.append(teamData)
    
#File to save out to, will overwrite if script is rerun.
f = open("iri" + str(YEAR) + ".csv", 'w', encoding='utf-8')

#write out names of data fields. This is kind of bad and uses data from the last
#loop execution to get field names.
for prop in teamData.keys():
    f.write(prop + ", ")
f.write("\n")

#iterate over the teams we got data for and write out their data.
for team in teamsList:
    for prop in team.keys():
        f.write(str(team[prop]) + ", ")
    f.write("\n")
f.close()