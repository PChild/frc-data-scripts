import gen

tba = gen.setup()

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

gen.listOfDictToCSV("iriNoFinals", noFinals)