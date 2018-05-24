import tbapy
import pandas as pd
import trueskill

tba = tbapy.TBA('DJRE7IGB1IBTCtvpZfFnn7aZfBWoY9bTIZfQFY7CVBZ8tWeNRX6x0XdISQ63skHv')

YEAR = 2018
DISTRICT = 'chs'


tieData = pd.read_csv('tieData.csv').set_index('year')
matches = tieData.loc[YEAR][0]
ties = tieData.loc[YEAR][1]

allTeams = {}

trueskill.DRAW_PROBABILITY = ties / matches

events = tba.district_events(str(YEAR) + DISTRICT, True, False)
events = sorted(events, key = lambda k: k['start_date'])

for event in events:
    print("Processing " + event['key'])
    for team in tba.event_teams(event['key'], True, True):
        if team not in allTeams:    
            allTeams[team] = {'team': team[3:], 'mu': 25, 'sigma': 8.333, 'matches': 0, 'history': ''}
    
    matches = tba.event_matches(event['key'], True, False)        
    matches = sorted(matches, key = lambda k: k['time'])
    
    for match in matches:
        matchAlliances = []
        
        redAlliance = {}
        blueAlliance = {}
                      
                        
        winner = match['winning_alliance']
        
        redWin = 1 - (winner == 'red' or winner == '')
        blueWin =  1 - (winner == 'blue' or winner == '')
            
        for redTeam in match['alliances']['red']['team_keys']:
            redAlliance[redTeam] = trueskill.Rating(allTeams[redTeam]['mu'], allTeams[redTeam]['sigma'])                        
            
        for blueTeam in match['alliances']['blue']['team_keys']:                    
            blueAlliance[blueTeam] = trueskill.Rating(allTeams[blueTeam]['mu'], allTeams[blueTeam]['sigma'])
            
        redAlliance, blueAlliance = trueskill.rate([redAlliance, blueAlliance], [redWin, blueWin])
        
        for teamRed in redAlliance:
            curr = allTeams[teamRed]
            curr['mu'] = redAlliance[teamRed].mu
            curr['sigma'] = redAlliance[teamRed].sigma
            curr['matches'] += 1
            curr['history'] += " / " + str(round(redAlliance[teamRed].mu, 1))
        
        for teamBlue in blueAlliance:
            curr = allTeams[teamBlue]
            curr['mu'] = blueAlliance[teamBlue].mu
            curr['sigma'] = blueAlliance[teamBlue].sigma
            curr['matches'] += 1
            curr['history'] += " / " + str(round(blueAlliance[teamBlue].mu, 1))

#File to save out to, will overwrite if script is rerun.

chsTeams = tba.district_teams(str(YEAR)+ DISTRICT, True, True)

nonCHS = []
for team in allTeams:
    if not team in chsTeams:
        nonCHS.append(team)

for team in nonCHS:        
    allTeams.pop(team)

f = open(DISTRICT + "TrueSkill.csv", 'w', encoding='utf-8')

#write out names of data fields.
for prop in allTeams[next(iter(allTeams))].keys():
    f.write(prop + ", ")
f.write("\n")

#iterate over the teams we got data for and write out their data.
for team in allTeams:
    for prop in allTeams[team].keys():
        f.write(str(allTeams[team][prop]) + ", ")
    f.write("\n")
f.close()