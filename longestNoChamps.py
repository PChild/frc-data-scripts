import gen

currentTeams = gen.readTeamListCsv(2019)

teamGaps = {x : {'Max Gap': 0, 'Current Gap': 0} for x in currentTeams['Teams']}

for year in range(1992, 2019):
    yearTeams = gen.readTeamListCsv(year)
    
    for team in currentTeams['Teams']:
        entry = teamGaps[team] 
        if team in yearTeams['Teams'].unique():
            teamYearEvents = gen.readTeamCsv(team, 'events', year)
            
            
            champTypes = [3, 4]
            if any(elem in champTypes for elem in teamYearEvents['Type']):
                if entry['Current Gap'] > entry['Max Gap']:
                    entry['Max Gap'] = entry['Current Gap']
                    entry['Current Gap'] = 0
            else:
                entry['Current Gap'] += 1
                
for team in teamGaps:
    entry = teamGaps[team]
    if entry['Current Gap'] > entry['Max Gap']:
        entry['Max Gap'] = entry['Current Gap']