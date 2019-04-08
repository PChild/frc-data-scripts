import gen

tba = gen.setup()

maxPages = 20

finalistTeams = []
for i in range(0, maxPages):    
    
    gen.progressBar(i, maxPages)

    teams = tba.teams(i, None, False, True)
    
    if teams == []:
        break
    
    for team in teams:
        
        finalist = 0        
        
        for award in tba.team_awards(team):
            if award['award_type'] == 2:
                finalist += 1
            elif award['award_type'] == 1:
                break
        finalistTeams.append({'Team': team[3:], 'Finalist Count': finalist})

finalistTeams = sorted(finalistTeams, key = lambda k: k['Finalist Count'], reverse=True)

colOrder = ['Team', 'Finalist Count']
gen.listOfDictToCSV("finalistTeams", finalistTeams, colOrder)