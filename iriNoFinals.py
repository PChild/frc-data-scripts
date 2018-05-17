import tbapy

tba = tbapy.TBA('DJRE7IGB1IBTCtvpZfFnn7aZfBWoY9bTIZfQFY7CVBZ8tWeNRX6x0XdISQ63skHv')

noFinals = []

for year in range(2012, 2018):
    print("Processing " + str(year))
    teams = tba.event_teams(str(year)+"iri", True, True)
    
    for team in teams:
        awards = tba.team_awards(team, year)

        madeFinals = False        
        
        for award in awards:
            madeFinals = madeFinals or award['award_type'] in [1,2]
        
        if not madeFinals:
            print("Team " + str(team[3:]) + " missed finals in " + str(year))
            noFinals.append({'team': team[3:], 'year': year})

for team in noFinals:
    madeElims = False    
    
    for match in tba.team_matches(int(team['team']), str(team['year'])+'iri', int(team['year']), True, False)   :
        if match['comp_level'] != "qm":
            madeElims = True
    
    team['iriElims'] = madeElims

for team in noFinals:
    madeElims = False    
    
    for match in tba.team_matches(int(team['team']), None, int(team['year']), True, False):
        if match['comp_level'] != "qm":
            madeElims = True
    
    team['elims'] = madeElims

f = open("iriNoFinals.csv", 'w', encoding='utf-8')

for prop in team:
    f.write(prop + ", ")
f.write("\n")

for team in noFinals:
    for prop in team:
        f.write(str(team[prop]) + ", ")
    f.write("\n")
f.close()