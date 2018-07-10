import gen

tba = gen.setup()

data = []
years = range(2011, 2018)
for idx, year in enumerate(years):
    gen.progressBar(idx, len(years))
    
    teamCount = 0
    
    for page in range(0, 20):
        yearTeams = tba.teams(page, year)
        if yearTeams != []:
            for team in yearTeams:
                if team['state_prov'] in ['NY', 'New York']:
                    teamMatches = tba.team_matches(team['team_number'], None, year, False, True)
                    
                    if len(teamMatches) > 0:
                        teamCount += 1
        else:
            break
    data.append({'Year': year, 'Count': teamCount})
gen.listOfDictToCSV("nyTeams", data)