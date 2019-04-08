import tbapy
import csv
import statistics as stat

TEAM = 401
YEAR = '2018'

tba = tbapy.TBA('DJRE7IGB1IBTCtvpZfFnn7aZfBWoY9bTIZfQFY7CVBZ8tWeNRX6x0XdISQ63skHv')

matches = []
teamList = []
teamData = {}
matchKeys = ['r1', 'r2', 'r3', 'b1', 'b2', 'b3']

def calcStats(values):
    meanVal = stat.mean(values)
    medVal = stat.median(values)
    minVal = min(values)
    maxVal = max(values)
    stdDev = stat.stdev(values)
    
    return [meanVal, medVal, minVal, maxVal, stdDev]

# Match, Blue 1, Blue 2, Blue 3, Red 1, Red 2, Red 3
with open(str(TEAM) + 'in.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        match = {'num': row[0], 'b1': row[1], 'b2': row[2], 'b3': row[3], 'r1': row[4], 'r2': row[5], 'r3': row[6]}
        
        for val in matchKeys:
            teamList.append(int(match[val]))
            
        matches.append(match)

teamList = sorted(list(set(teamList)))

for team in teamList:
    teamData[str(team)] = {'num': team, 'oprs': [], 'ccwms': [], 'dprs': [], 'autoScale': [], 'autoSwitch': [], 'teleScale': [], 'teleSwitch': [], 'vaultPoints': [], 'endgamePoints': [], 'autoQuest': 0, 'faceBoss': 0, 'matches': 0}
    
    teamEvents = tba.team_events(team, YEAR)
    print(team)

    for event in teamEvents:
        if event['event_type'] < 3:
            try:
                eventStats = tba.event_oprs(event['key'])
                teamMatches = tba.team_matches(team, event['key'])
                
                teamOpr = eventStats['oprs']["frc" + str(team)]
                teamCcwm = eventStats['ccwms']["frc" + str(team)]
                teamDpr = eventStats['dprs']["frc" + str(team)]
                
                teamEntry = teamData[str(team)]
                
                teamEntry['oprs'].append(teamOpr)
                teamEntry['ccwms'].append(teamCcwm)
                teamEntry['dprs'].append(teamDpr)
                
                for match in teamMatches:
                    teamEntry['matches'] += 1
                    
                    teamKey = "frc" + str(team)
                    teamColor = "red"
                    
                    blueTeams = match['alliances']['blue']['team_keys']
                    redTeams = match['alliances']['red']['team_keys']
                    
                    if teamKey in blueTeams:
                        teamPos = blueTeams.index(teamKey)
                        teamColor = "blue"
                    else:
                        teamPos = redTeams.index(teamKey)
                        teamColor = "red"
                        
                    matchData = match['score_breakdown'][teamColor]
                    
                    teamEntry['autoScale'].append(matchData['autoScaleOwnershipSec'])
                    teamEntry['autoSwitch'].append(matchData['autoSwitchOwnershipSec'])
                    teamEntry['teleScale'].append(matchData['teleopScaleOwnershipSec'])
                    teamEntry['teleSwitch'].append(matchData['teleopSwitchOwnershipSec'])
                    teamEntry['vaultPoints'].append(matchData['vaultPoints'])
                    teamEntry['endgamePoints'].append(matchData['endgamePoints'])
                    teamEntry['autoQuest'] += matchData['autoQuestRankingPoint']
                    teamEntry['faceBoss'] += matchData['faceTheBossRankingPoint']
            except:
                pass
# Min, Max, Median, Mean
f = open(str(TEAM) + "out.csv", 'w')

f.write('Team, Matches Played, Mean OPR, Median OPR, Min OPR, Max OPR, Std Dev OPR, Mean CCWM, Median CCWM, Min CCWM, Max CCWM, Std Dev CCWM, Mean DPR, Median DPR, Min DPR, Max DPR, Std Dev DPR, Mean Auto Scale, Median Auto Scale, Min Auto Scale, Max Auto Scale, Std Dev Auto Scale, Mean Auto Switch, Median Auto Switch, Min Auto Switch, Max Auto Switch, Mean Teleop Scale, Median Teleop Scale, Min Teleop Scale, Max Teleop Scale, Std Dev Teleop Scale, Mean Teleop Switch, Median Teleop Switch, Min Teleop Switch, Max Teleop Switch, Std Dev Teleop Switch, Mean Vault Points, Median Vault Points, Min Vault Points, Max Vault Points, Std Dev Vault Points, Mean Endgame Points, Median Endgame Points, Min Endgame Points, Max Endgame Points, Std Dev Endgame Points, Face the Boss Percent, Auto Quest Percent\n')

for team in teamData:
    number = team['num']
    matches = team['matches']
    meanOPR, medOPR, minOPR, maxOPR, sdOPR = calcStats(team['oprs'])
    meanCCWM, medCCWM, minCCWM, maxCCWM, sdCCWM = calcStats(team['ccwms'])
    meanDPR, medDPR, minDPR, maxDPR, sdDPR = calcStats(team['dprs'])
    
    meanAS, medAS, minAS, maxAS, sdAS = calcStats(team['autoScale'])
    meanASw, medASw, minASw, maxASw, sdASw = calcStats(team['autoSwitch'])
    meanTS, medTS, minTS, maxTS, sdTS = calcStats(team['teleScale'])
    meanTSw, medTSw, minTSw, maxTSw, sdTSw = calcStats(team['teleSwitch'])
    meanVP, medVP, minVP, maxVP, sdVP = calcStats(team['vaultPoints'])
    meanEP, medEP, minEP, maxEP, sdEP = calcStats(team['endgamePoints'])
    
    meanFaceBoss = team['faceBoss'] / team['matches'] * 100
    meanAutoQuest= team['autoQuest'] / team['matches'] * 100
    
    dataFields = [number, matches,
                  meanOPR, medOPR, minOPR, maxOPR, sdOPR,
                  meanCCWM, medCCWM, minCCWM, maxCCWM, sdCCWM,
                  meanDPR, medDPR, minDPR, maxDPR, sdDPR,
                  meanAS, medAS, minAS, maxAS, sdAS,
                  meanASw, medASw, minASw, maxASw, sdASw,
                  meanTS, medTS, minTS, maxTS, sdTS,
                  meanTSw, medTSw, minTSw, maxTSw, sdTSw,
                  meanVP, medVP, minVP, maxVP, sdVP,
                  meanEP, medEP, minEP, maxEP, sdEP,
                  meanFaceBoss, meanAutoQuest]
    
    for item in dataFields:
        f.write(str(item) + ", ")
    f.write('\n')
f.close()