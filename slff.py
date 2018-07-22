import gen
from scipy.special import erfinv
import statistics as stat
import math

tba = gen.setup()
VALIDATE = False
isDistrict = False

eventData = {}
def getPerformanceData(team):
    oprs = []
    wins = 0
    losses = 0
    ties = 0
    
    try:
        matches = tba.team_matches(team, None, YEAR, True, False)    
        if len(matches) > 0:
            for match in matches:       
                wins += 'win' == gen.matchResult(team, match)
                losses += 'loss' == gen.matchResult(team, match)
                ties += 'tie' == gen.matchResult(team, match)
    except:
        print("Could not retrieve matches for", team)
        
    try:
        events = tba.team_events(team, YEAR)
        if len(events) > 0:    
            for event in events:
                if event['event_type'] in range(0,10):
                    try:
                        if event['key'] in eventData.keys():
                            oprs.append(eventData[event['key']]['oprs'][team])
                        else:
                            print("Storing event " + event['key'])
                            eventData[event['key']]  = tba.event_oprs(event['key'])
                            oprs.append(eventData[event['key']]['oprs'][team])
        
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
    winPercent = .3
    
    if played > 0:
        winPercent = wins / played
    
    teamKey = team
    if team[:3] == "frc":
        teamKey = team[3:]
    
    return {'Team': teamKey, 
            'Max OPR': maxOPR, 
            'Avg OPR': avgOPR, 
            'Wins': wins, 
            'Losses': losses, 
            'Ties': ties, 
            'Win %': winPercent}

def calcPoints(team, event):
    teamMatches = tba.team_matches(team, event, None, True)
    draftPoints = 0
    rankPoints = 0
    elimPoints = 0
     
    if teamMatches != []:
        try:
            #Use team status instead of event_district_points since SLFF counts elims and awards points differently...
            teamStats = tba.team_status(team, event)
            #Find draft points
            alliance = teamStats['alliance']           
            if alliance:
                if alliance['pick'] < 2:
                    draftPoints = 17 - alliance['number']
                elif alliance['pick'] == 2:
                    draftPoints = alliance['number']

            #Find quals ranking points
            teamCount = teamStats['qual']['num_teams']
            teamRank = teamStats['qual']['ranking']['rank']
            alpha = 1.07
            rankPoints = math.ceil(abs(erfinv( (teamCount - 2 * teamRank + 2) /  (alpha * teamCount)) * 10 / erfinv( 1 / alpha ) + 12 ))
        except:
            pass
    
        #Find points for playing in elims
        for match in teamMatches:
            if match['comp_level'] != "qm":
                if gen.matchResult(team, match) == 'win':
                    elimPoints += 5
    
    return draftPoints + rankPoints + elimPoints

def teamAtEvent(team, event):
    ROBOT_AWARDS = [16, 17, 20, 21, 29, 71]
    OTHER_AWARDS = [1, 2, 5, 11, 13, 14, 18, 22, 27, 30]
    CA = 0
    EI = 9
    WF = 3
    DEANS = 4
    RAS = 10
    RI = 15
    CAF = 69
    WILDCARD = 68
    
    awardData = {'REG': {CA: 60, EI: 45, RAS: 25, RI: 15, WF: 10, DEANS: 5, WILDCARD: 0, 'ROBOT': 20, 'OTHER': 5},
                 'CMP': {CA: 110, EI: 60, RAS: 35, RI: 20, WF: 30, DEANS: 15, CAF: 90, 'ROBOT': 30, 'OTHER': 10}}
                 
                 
    #Fetch event info, do this first since we only want to really process official events.             
    eventInfo = tba.event(event, True)
    
    isOfficial = eventInfo['event_type'] in range(0, 7)
    isChamps = eventInfo['event_type'] in range(3, 5)

    awardPoints = 0
    playPoints = 0
    
    if isOfficial:
        teamAwards = tba.team_awards(team, None, event)
        playPoints = calcPoints(team, event)
            
        #Process awards at the event, handle champs vs regular events.
        eventType = 'CMP' if isChamps else 'REG'
        for award in teamAwards:
            awardType = award['award_type']
            
            if awardType in ROBOT_AWARDS:
                awardType = 'ROBOT'
            
            if awardType in OTHER_AWARDS:
                awardType = 'OTHER'
            awardPoints += awardData[eventType][awardType]
            
    return [playPoints, awardPoints]

def getTeamRatingData(team, yearDepth=3):
    overallRating = 0
    playRating = 0
    teamTotal = 0
    eventMax = 0
    eventCount = 0
    eventAvg = 0
    teamYears = tba.team_years(team)
    
    try:
        pastYears = sorted(teamYears[-yearDepth:], key=int, reverse=True)
        
        tmpYears = pastYears[:]
                    
        for year in tmpYears:
            if year < YEAR - yearDepth:
                pastYears.remove(year)
        for count, year in enumerate(pastYears):
            yearPoints = 0
            yearPlayPoints = 0
            
            for event in tba.team_events(team, year, False, True):
                eventPlayPoints, eventAwardPoints = teamAtEvent(team, event)
                eventPoints = eventPlayPoints + eventAwardPoints            
                yearPoints += eventPoints
                yearPlayPoints += eventPlayPoints
                if eventPoints > 0:
                    eventCount += 1
                eventMax = eventPoints if eventPoints > eventMax else eventMax
            
            playRating += yearPlayPoints / pow(2, count * 2)
            overallRating += yearPoints / pow(2, count * 2)
            teamTotal += yearPoints
        eventAvg = teamTotal / eventCount
    except Exception as e:
        print(e)
        
    teamKey = team
    if team[:3] == "frc":
        teamKey = team[3:]
    
    return {'Team': teamKey, 
            'Overall Rating': overallRating, 
            'Event Max': eventMax, 
            'Total Points': teamTotal, 
            'Year Avg': teamTotal / yearDepth, 
            'Event Avg': eventAvg, 
            'Events': eventCount, 
            'Play Rating': playRating}

def buildDraftList(key, isDistrict, eventTeams=None):
    if eventTeams:
      teamList = eventTeams  
    elif isDistrict:
        teamList = tba.district_teams(key, False, True)
    else:
        teamList = tba.event_teams(key, False, True)
    listData = []
    for idx, team in enumerate(teamList):
        print(team)
        ratingData = getTeamRatingData(team)
        perfData = getPerformanceData(team)
        
        perfData.update(ratingData)        
        
        listData.append(perfData)
    return listData

YEAR = 2018
#KEY = "rbcn"
#eventCode = str(YEAR) + KEY
#
#rcTeams = ['frc4362','frc5712' ]
#
#fileName = eventCode
#teamData = buildDraftList(None, False, rcTeams)
#
#
#
#if VALIDATE:
#    fileName += "Validate"
#    for team in teamData:
#        team['actual'] = calcPoints(int(team['Team #']), eventCode)
#    
#colOrder = ['Team', 'Avg OPR', 'Max OPR', 'Win %', 'Wins', 'Losses', 'Ties', 'Play Rating', 'Overall Rating', 'Total Points', 'Event Max', 'Event Avg', 'Year Avg', 'Events']        
#gen.listOfDictToCSV(fileName, teamData, colOrder)
