import gen
from scipy.special import erfinv

tba = gen.setup()
YEAR = 2018
KEY = "txsc"
isDistrict = False


def calcPoints(team, event):
    teamMatches = tba.team_matches(team, event, None, True)
    draftPoints = 0
    rankPoints = 0
    elimPoints = 0
     
    if teamMatches != []:
        try:
            #Use team status instead of event_district_points since SLFF counts elims and awards points differently..s
            teamStats = tba.team_status(team, event)
            #Find draft points
            alliance = teamStats['alliance']           
            if alliance:
                if alliance['pick'] < 2:
                    draftPoints = 17 - alliance['number']
                else:
                    draftPoints = alliance['number']

            #Find quals ranking points
            teamCount = teamStats['qual']['num_teams']
            teamRank = teamStats['qual']['ranking']['rank']
            alpha = 1.07
            rankPoints = int(abs(erfinv( (teamCount - 2 * teamRank + 2) /  (alpha * teamCount)) * 10 / erfinv( 1 / alpha ) + 12 ) + .5)
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
    pastYears = sorted(tba.team_years(team)[-yearDepth:], key=int, reverse=True)
    
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
        
        playRating += yearPlayPoints / pow(2, count)
        overallRating += yearPoints / pow(2, count)
        teamTotal += yearPoints
    eventAvg = teamTotal / eventCount
    return {'Team #': team[3:], 
            'Overall Rating': overallRating, 
            'Event Max Points': eventMax, 
            'Total Points': teamTotal, 
            'Year Avg': teamTotal / yearDepth, 
            'Event Avg': eventAvg, 
            'Events': eventCount, 
            'playRating': playRating}

def buildDraftList(key, isDistrict):
    if isDistrict:
        teamList = tba.district_teams(key, False, True)
    else:
        teamList = tba.event_teams(key, False, True)
    listData = []
    for idx, team in enumerate(teamList):
        gen.progressBar(idx, len(teamList))
        listData.append(getTeamRatingData(team))
    return listData

eventCode = str(YEAR) + KEY
teamData = buildDraftList(eventCode, isDistrict)

for team in teamData:
    team['actual'] = calcPoints(int(team['Team #']), eventCode)
    
gen.listOfDictToCSV(eventCode + "Validate", teamData)