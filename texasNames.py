import gen

tba = gen.setup()

teams = tba.district_teams('2019tx')

mapTeams = []
for team in teams:
    mapTeams.append({'Team': team['team_number'], 'Name': team['nickname']})
    
gen.listOfDictToCSV('Texas Names', mapTeams, ['Team', 'Name'])