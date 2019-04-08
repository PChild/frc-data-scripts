import gen

tba = gen.setup()

chsTeams = []
for team in tba.district_teams('2016chs', True):
    chsTeams.append(team['team_number'])

chsLocations =  ['Virginia', 'Maryland', 'District of Columbia', 'DC', 'VA, ''MD']
allTeams = []
foundChsTeams = []

        
for page in range(0,20):
    try:
        newTeams = tba.teams(page, 2016, True)
        
        if newTeams == []:
            print("Broke on page", page)            
            break;
        else:
            allTeams += newTeams
    except:
        pass

for team in allTeams:
    if team['state_prov'] in chsLocations:
        foundChsTeams.append(team['team_number'])
        
print("Found", len(foundChsTeams), "out of", len(chsTeams))
for team in chsTeams:
    if team not in foundChsTeams:
        print("Missed", team)
        
for team in foundChsTeams:
    if team not in chsTeams:
        print("Mistakenly found", team)