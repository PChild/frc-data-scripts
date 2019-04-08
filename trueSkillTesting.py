import tbapy
import pandas as pd
import trueskill
import json

tba = tbapy.TBA('DJRE7IGB1IBTCtvpZfFnn7aZfBWoY9bTIZfQFY7CVBZ8tWeNRX6x0XdISQ63skHv')
tieData = pd.read_csv('tieData.csv').set_index('year')


allTeams = {}
YEARS = [2010, 2011, 2012, 2013, 2014, 2016, 2017, 2018]

def calcMatchRank(match):
    levels =  {'qm': 1, 'qf': 10, 'sf': 100, 'f': 1000}
    
    return levels[match['comp_level']] + match['match_number'] 

for page in range(0,20):
    print("Fetching team page " + str(page))
    for team in tba.teams(page, None, True, True):
        allTeams[team] = {'team': team[3:], 'mu': 25, 'sigma': 8.333, 'years': {}}
            
for year in YEARS:
    print("Processing " + str(year))
    matches = tieData.loc[year][0]
    ties = tieData.loc[year][1]
    trueskill.DRAW_PROBABILITY = ties / matches
    
    for team in allTeams:
        allTeams[team]['years'][str(year)] = {}
        allTeams[team]['mu'] = 25
        allTeams[team]['sigma'] = 8.333
    
    events = tba.events(year, True, False)
    events = sorted(events, key = lambda k: k['start_date'])
    
    print("Got " + str(len(events)) + " events")    
    
    for event in events:
        if event['event_type'] in range(0,10):
            teams = tba.event_teams(event['key'], True, True)
            
            matches = tba.event_matches(event['key'], True, False)
            matches = sorted(matches, key = lambda match: calcMatchRank(match))
            
            print("Processing " + str(len(matches)) + " matches for " + event['key'])
            
            for match in matches:
                redAlliance = []
                blueAlliance = []
                
                redTeams = []
                blueTeams = []                
                                
                winner = match['winning_alliance']
                
                redWin = 1 - (winner == 'red' or winner == 'tie')
                blueWin =  1 - (winner == 'blue' or winner == 'tie')
                
                for team in match['alliances']['red']['team_keys']:
                    redTeams.append(team)
                    teamRating = trueskill.Rating(allTeams[team]['mu'], allTeams[team]['sigma'])                        
                    redAlliance.append(teamRating)
                    
                for team in match['alliances']['blue']['team_keys']:
                    blueTeams.append(team)                    
                    teamRating = trueskill.Rating(allTeams[team]['mu'], allTeams[team]['sigma'])                        
                    blueAlliance.append(teamRating)

                redAlliance, blueAlliance = trueskill.rate([redAlliance, blueAlliance], [redWin, blueWin])
                
                for team in redAlliance:
                    allTeams[redTeams[redAlliance.index(team)]]['mu'] = team.mu
                    allTeams[redTeams[redAlliance.index(team)]]['sigma'] = team.sigma
            
            for team in teams:
                allTeams[team]['years'][str(year)][event['key']] = {}
                allTeams[team]['years'][str(year)][event['key']]['mu'] = allTeams[team]['mu']
                allTeams[team]['years'][str(year)][event['key']]['sigma'] = allTeams[team]['sigma']

with open('TrueSkills.json', 'w') as outfile:
    json.dump(allTeams, outfile)