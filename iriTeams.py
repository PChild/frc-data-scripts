import pandas as pd
import statistics as stat
import gen

tba = gen.setup()

YEAR = 2019

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
    
gen.listOfDictToCSV("iri" + str(YEAR), teamsList)