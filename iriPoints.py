import gen
from scipy.special import erfinv
import math

tba = gen.setup()
EVENT = '2018iri'
teams = tba.event_teams(EVENT, False, True)
teams.append('frc2363')
teamCount = len(teams)

eventRanks = tba.event_rankings('2018iri')['rankings']
rankings = {}
for tm in eventRanks:
    rankings[tm['team_key']] = tm['rank'] 

def calcPoints(team, event):
    teamRank = rankings[team]
    draftPoints = 0
    rankPoints = 0
    elimPoints = 0          

    alpha = 1.07
    rankPoints = math.ceil(abs(erfinv( (teamCount - 2 * teamRank + 2) /  (alpha * teamCount)) * 10 / erfinv( 1 / alpha ) + 12 ))
     
    teamMatches = tba.team_matches(team, event, None, True)
    if teamMatches != []:
        try:
            #Use team status instead of event_district_points since SLFF counts elims differently
            teamStats = tba.team_status(team, event)
            
            #Find draft points
            alliance = teamStats['alliance']           
            if alliance:
                if alliance['pick'] < 2:
                    draftPoints = 17 - alliance['number']
                if alliance['pick'] == 2:
                    #IRI, second draft round is reversed
                    draftPoints =  9 - alliance['number']
        except:
            pass
    
        #Find points for playing in elims
        for match in teamMatches:
            if match['comp_level'] != "qm":
                if gen.matchResult(team, match) == 'win':
                    elimPoints += 5
    
    return [teamRank, draftPoints, rankPoints, elimPoints]

teamData = []

for idx, team in enumerate(teams):
    gen.progressBar(idx, teamCount)
    rank, draft, rankP, elim = calcPoints(team, EVENT)
    total = draft + rankP + elim
    teamData.append({'team': team[3:], 'rank': rank, 'total': total, 'rankP': rankP, 'draft': draft, 'elim': elim})
    
colOrder = ['team', 'rank', 'total', 'rankP', 'draft', 'elim']
gen.listOfDictToCSV('iriPoints', teamData, colOrder)