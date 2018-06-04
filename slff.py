import gen
from scipy.special import erfinv

tba = gen.setup()
YEAR = 2018
yearDepth = 3

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
        
    rankPoints = 0
    draftPoints = 0
    elimPoints = 0
    awardPoints = 0
    
    if isOfficial:
        teamMatches = tba.team_matches(team, event, None, True)
        teamAwards = tba.team_awards(team, None, event)
         
        if teamMatches != []:
            try:
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
            
        #Process awards at the event, handle champs vs regular events.
        eventType = 'CMP' if isChamps else 'REG'
        for award in teamAwards:
            awardType = award['award_type']
            
            if awardType in ROBOT_AWARDS:
                awardType = 'ROBOT'
            
            if awardType in OTHER_AWARDS:
                awardType = 'OTHER'
            awardPoints += awardData[eventType][awardType]
            
    return rankPoints + draftPoints + elimPoints + awardPoints

teamRatings = []

for page in range(0,20):
    print("On page", page)    
    pageTeams = tba.teams(page, YEAR, False, True)
    
    if pageTeams == []:
        break
    else:
        for team in pageTeams:
            teamRating = 0
            teamTotal = 0
            teamMax = 0
            teamNum = int(team[3:])
            pastYears = sorted(tba.team_years(team)[-yearDepth:], key=int, reverse=True)
            
            tmpYears = pastYears[:]
            
            for year in tmpYears:
                if year < YEAR - yearDepth:
                    pastYears.remove(year)
            for count, year in enumerate(pastYears):
                yearPoints = 0
                
                for event in tba.team_events(teamNum, year, False, True):
                    yearPoints += teamAtEvent(teamNum, event)
                    
                teamRating += yearPoints / pow(2, count)
                teamMax = yearPoints if yearPoints > teamMax else teamMax
                teamTotal += yearPoints
            teamRatings.append({'team': teamNum, 'rating': teamRating, 'max': teamMax, 'total': teamTotal, 'avg': teamTotal / yearDepth})
            print("Finished team", team)
gen.listOfDictToCSV("slffRatings", teamRatings)