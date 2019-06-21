import gen

tba = gen.setup()

team = 'frc33'

tripleMatches = []
bestClimb = [0, '']
for match in tba.team_matches(team, year=2019):
    teamColor = 'blue' if team in match['alliances']['blue']['team_keys'] else 'red'
    
    climbPts = match['score_breakdown'][teamColor]['habClimbPoints']
    
    if climbPts == 36:
        tripleMatches.append(match['key'])
    
    if climbPts > bestClimb[0]:
        bestClimb = [climbPts, match['key']]
        
print(tripleMatches)
print(bestClimb)