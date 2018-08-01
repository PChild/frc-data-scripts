import gen
from scipy.special import erfinv
import statistics as stat
from pathlib import Path
import math

tba = gen.setup()
VALIDATE = False
isDistrict = False

def getPerformanceData(team, year):
    team = gen.teamString(team)
    oprs = []
    wins = 0
    losses = 0
    ties = 0
    
    try:
        matches = gen.readTeamCsv(team, 'matches', year)  
        if len(matches) > 0:
            for idx, match in matches.iterrows():
                result = gen.matchResult(team, match)
                wins += 'WIN' == result
                losses += 'LOSS' == result
                ties += 'TIE' == result
    except:
        print("Could not retrieve matches for", team)
        
    try:
        events = gen.readTeamCsv(team, 'events', year)
        if len(events) > 0:    
            for idx, e in events.iterrows():                    
                    try:
                        eOprs = gen.readEventCsv(e['Event'], 'opr')
                        teamOPR = eOprs[eOprs.Team == team]['OPR'].values[0]
                        oprs.append(teamOPR)
                    except Exception as e:
                        print(e)
    except:
        print("Could not retrieve events for", team)
        
        
    if len(oprs) is 0:
        maxOPR = 0
        avgOPR = 0
    else:
        maxOPR = max(oprs)
        avgOPR = stat.mean(oprs)
    
    played = wins + losses + ties
    winPercent = 0
    
    if played > 0:
        winPercent = wins / played
    
    teamKey = gen.teamNumber(team)
    
    return {'Team': teamKey, 
            'Max OPR': maxOPR, 
            'Avg OPR': avgOPR, 
            'Wins': wins, 
            'Losses': losses, 
            'Ties': ties, 
            'Win %': winPercent}

def getTeamYears(team, YEAR):
    team = gen.teamString(team)    
    teamYears = []
    repo = gen.getRepoPath()
    
    for year in range(1992, YEAR + 1):
        yearPath = Path(repo + 'teams/' + str(year) + '/' + team + '/')
        
        if yearPath.exists():
            teamYears.append(year)
    return teamYears
            
def getAwardPoints(team, event, eventType, useTba=False):
    ROBOT_AWARDS = [16, 17, 20, 21, 29, 71]
    OTHER_AWARDS = [ 5, 11, 13, 14, 18, 22, 27, 30]
    NO_POINTS = [1, 2]
    CA = 0
    EI = 9
    WF = 3
    DEANS = 4
    RAS = 10
    RI = 15
    CAF = 69
    WILDCARD = 68
    
    awardData = {'REG': {CA: 60, EI: 45, RAS: 25, RI: 15, WF: 10, DEANS: 5, WILDCARD: 0, 'ROBOT': 20, 'OTHER': 5, 'NONE': 0},
                 'CMP': {CA: 110, EI: 60, RAS: 35, RI: 20, WF: 30, DEANS: 15, CAF: 90, 'ROBOT': 30, 'OTHER': 10, 'NONE': 0}}
    
    awardPoints = 0
    
    if useTba:
        try:
            tya = tba.team_awards(team, None, event)
            for award in tya:
                awardType = award['award_type']
                
                if awardType in ROBOT_AWARDS:
                    awardType = 'ROBOT'
                if awardType in OTHER_AWARDS:
                    awardType = 'OTHER'
                if awardType in NO_POINTS:
                    awardType = 'NONE'
                awardPoints += awardData[eventType][awardType]
        except:
            pass
    else:
        tya = gen.readTeamCsv(team, 'awards', event[:4])
        if tya is not None:
            teamEventAwards = tya[tya.Event == event]
            
            for idx, row in teamEventAwards.iterrows():
                awardType = row['Type']
                
                if awardType in ROBOT_AWARDS:
                    awardType = 'ROBOT'
                if awardType in OTHER_AWARDS:
                    awardType = 'OTHER'
                if awardType in NO_POINTS:
                    awardType = 'NONE'
                awardPoints += awardData[eventType][awardType]
    return awardPoints

def getPlayPoints(team, event, eventType, useTba=False, breakDown=False, eventSize=None):
    draftPoints = 0
    rankPoints = 0
    elimPoints = 0
    
    if useTba == True:
        try:
            teamMatches = tba.team_matches(team, event, None, True)
            teamStats = tba.team_status(team, event)
            
            alliance = teamStats['alliance']           
            if alliance is not None:
                if alliance['pick'] < 2:
                    draftPoints = 17 - alliance['number']
                elif alliance['pick'] == 2:
                    draftPoints = alliance['number']
            if eventSize is not None:
                teamCount = eventSize
            else:
                teamCount = teamStats['qual']['num_teams']
                
            teamRank = teamStats['qual']['ranking']['rank']
            alpha = 1.07
            rankPoints = math.ceil(abs(erfinv( (teamCount - 2 * teamRank + 2) /  (alpha * teamCount)) * 10 / erfinv( 1 / alpha ) + 12 ))
                
            for match in teamMatches:
                if match['comp_level'] != "qm":
                    if gen.matchResult(team, match, useTba) == 'WIN':
                        elimPoints += 5
        except:
            pass
    else:
        teamMatches = gen.teamEventMatches(team, event)
        
        tmpRk = []
        try:
            rK = gen.readEventCsv(event, 'rankings')
            tmpRk = rK[rK.Team == team]
        except:
            pass
        if len(tmpRk) > 0:
            teamRank = rK[rK.Team == team]['Rank'].iloc[0]
            teamCount = len(rK)
            
            alpha = 1.07
            rankPoints = math.ceil(abs(erfinv( (teamCount - 2 * teamRank + 2) /  (alpha * teamCount)) * 10 / erfinv( 1 / alpha ) + 12 ))
        
        names = ['captain', 'firstPick', 'secondPick']
        if eventType == 'CMP':
            names = ['captain', 'firstPick', 'secondPick', 'thirdPick']
        aL = gen.readEventCsv(event, 'alliances', names)
        if aL is not None:
            aLL = aL[(aL.captain == team) | (aL.firstPick == team) | (aL.secondPick == team)]
            if len(aLL) > 0:
                alliance = {'pick': 9, 'number': 9}
                alliance['number'] = aLL.index.values[0]
                
                if aLL['captain'].values[0] == team:
                    alliance['pick'] = 0
                elif aLL['firstPick'].values[0] == team:
                    alliance['pick'] = 1
                elif aLL['secondPick'].values[0] == team:
                    alliance['pick'] = 2
        
                if alliance['pick'] < 2:
                    draftPoints = 17 - int(alliance['number'])
                elif alliance['pick'] == 2:
                    draftPoints = int(alliance['number'])
    
        #Find points for playing in elims
        if teamMatches is not None:
            for idx, match in teamMatches.iterrows():
                if match['key'].split('_')[1][:2] != 'qm':
                    result = gen.matchResult(team, match, useTba)
                    
                    if result == 'WIN':
                        elimPoints += 5
    
    res = draftPoints + rankPoints + elimPoints
    if breakDown:
        res = [draftPoints, rankPoints, elimPoints] 
    return res

def getTeamEventPoints(team, event, useTba=False, eventSize=None):
    awardPoints = 0
    playPoints = 0

    team = gen.teamString(team)    

    if useTba == True:
        eventInfo = tba.event(event)
        isChamps = eventInfo['event_type'] in range(3,5)
    else:
        eventInfo = gen.readEventCsv(event, 'info')
        isChamps = eventInfo['Type'][0] in range(3, 5)
    eventType = 'CMP' if isChamps else 'REG'     
    
    if eventInfo is not None:
        playPoints = getPlayPoints(team, event, eventType, useTba, False, eventSize)
        awardPoints = getAwardPoints(team, event, eventType, useTba)
    return [playPoints, awardPoints]

def getTeamRatingData(team, yearDepth=3, YEAR=None):
    overallRating = 0
    playRating = 0
    teamTotal = 0
    eventMax = 0
    eventCount = 0
    eventAvg = 0
    team = gen.teamString(team)
    teamYears = getTeamYears(team, YEAR)
    
    pastYears = sorted(teamYears[-yearDepth:], key=int, reverse=True)
    
    tmpYears = pastYears[:]
                
    for year in tmpYears:
        if year < YEAR - yearDepth:
            pastYears.remove(year)
    for count, year in enumerate(pastYears):
        yearPoints = 0
        yearPlayPoints = 0
        
        for event in gen.readTeamCsv(team, 'events', year)['Event']:
            eventPlayPoints, eventAwardPoints = getTeamEventPoints(team, event)
            eventPoints = eventPlayPoints + eventAwardPoints            
            yearPoints += eventPoints
            yearPlayPoints += eventPlayPoints
            if eventPoints > 0:
                eventCount += 1
            eventMax = eventPoints if eventPoints > eventMax else eventMax
        
        playRating += yearPlayPoints / pow(2, count * 2)
        overallRating += yearPoints / pow(2, count * 2)
        teamTotal += yearPoints
        
    eventAvg = 0
    if eventCount > 0:
        eventAvg = teamTotal / eventCount
    
    teamKey = gen.teamNumber(team)
    
    return {'Team': teamKey, 
            'Overall Rating': overallRating, 
            'Event Max': eventMax, 
            'Total Points': teamTotal, 
            'Year Avg': teamTotal / yearDepth, 
            'Event Avg': eventAvg, 
            'Events': eventCount, 
            'Play Rating': playRating}

def buildDraftList(key, isDistrict, eventTeams=None, year=None):
    if eventTeams:
      teamList = eventTeams  
    elif isDistrict:
        teamList = tba.district_teams(key, False, True)
    else:
        teamList = tba.event_teams(key, False, True)
    listData = []
    for idx, team in enumerate(teamList):
        print(team)
        ratingData = getTeamRatingData(team, 1, year)
        perfData = getPerformanceData(team, year)
        
        perfData.update(ratingData)        
        
        listData.append(perfData)
    return listData

def teamListHelper(event):
    teams = []
    matches = tba.event_matches(event)
    for match in matches:
        for team in match['alliances']['red']['team_keys']:
            if team not in teams:
                teams.append(team)
        for team in match['alliances']['blue']['team_keys']:
            if team not in teams:
                teams.append(team)
    return teams

def scoreEvent(event):
    teams = teamListHelper(event)
    teamScores = sorted([{'Team': team[3:], 'Score': getTeamEventPoints(team, event, True, len(teams))[0]} for team in teams], key = lambda k: k['Score'], reverse=True)
    gen.listOfDictToCSV(event +"_scores", teamScores, ['Team', 'Score'])

def main():
    YEAR = 2018
    KEY = "wvrox"
    eventCode = str(YEAR) + KEY
    
    eventTeams = [48, 179, 456, 686, 888, 1038, 1629, 1732, 2614, 2655, 2656,
                  3260, 3492, 3504, 3538, 4265, 4462, 4467, 4505, 4575, 5549,
                  5740, 5811, 9999]
    #eventTeams = gen.readTeamListCsv(YEAR)['Teams'].tolist()
    
    fileName = eventCode
    teamData = buildDraftList(KEY, False, eventTeams, YEAR)
    
    if VALIDATE:
        fileName += "Validate"
        for team in teamData:
            team['actual'] = getTeamEventPoints(int(team['Team #']), eventCode)
        
    colOrder = ['Team', 'Avg OPR', 'Max OPR', 'Win %', 'Wins', 'Losses', 'Ties',
                'Play Rating', 'Overall Rating', 'Total Points', 'Event Max',
                'Event Avg', 'Year Avg', 'Events']        
    gen.listOfDictToCSV(fileName, teamData, colOrder)
if __name__ == '__main__':
    main()