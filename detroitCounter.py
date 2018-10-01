import gen

tba = gen.setup()

year = 2019

detTeams = 0
allTeams = 0
for page in range(0, 30):
    for team in tba.teams(page, year):
        allTeams += 1
        
        try:
            detTeams += team['home_championship']['2018'] == 'Detroit'
        except:
            print(team['key'])
            detTeams += 1
print(detTeams, '/', allTeams, 'at Detroit.')