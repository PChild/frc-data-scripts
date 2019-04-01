import gen

year = 2019

tba = gen.setup()

teams = []
for dist in tba.districts(year):
    teams += [int(team[3:]) for team in tba.district_teams(dist['key'], False, True)]
    
gen.listToCSV(str(year) +' District Teams', teams)