import tbapy
import pandas as pd
import trueskill

tba = tbapy.TBA('DJRE7IGB1IBTCtvpZfFnn7aZfBWoY9bTIZfQFY7CVBZ8tWeNRX6x0XdISQ63skHv')

YEAR = 2018
EVENT = '2018chcmp'

tieData = pd.read_csv('tieData.csv').set_index('year')
matches = tieData.loc[YEAR][0]
ties = tieData.loc[YEAR][1]

allTeams = {}

trueskill.DRAW_PROBABILITY = ties / matches

for team in tba.event_teams(EVENT, True, True):
    allTeams[team] = {'team': team[3:], 'mu': 25, 'sigma': 8.333, 'history': ''}

matches = tba.event_matches(EVENT, True, False)        
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
        curr['history'] += " / " + str(round(redAlliance[teamRed].mu, 1))
    
    for teamBlue in blueAlliance:
        curr = allTeams[teamBlue]
        curr['mu'] = blueAlliance[teamBlue].mu
        curr['sigma'] = blueAlliance[teamBlue].sigma
        curr['history'] += " / " + str(round(blueAlliance[teamBlue].mu, 1))

#File to save out to, will overwrite if script is rerun.
f = open(EVENT + "TrueSkill.csv", 'w', encoding='utf-8')

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