import gen
import slff
import statistics as stat

yearRange = 4
currentYear = 2018

tba = gen.setup()

teams = {}
for idx, year in enumerate(range(currentYear - yearRange + 1, currentYear + 1)):
    gen.progressBar(idx, currentYear + 1)
    
    for i in range(0,20):
        for team in tba.teams(i, year, False, True):
            if team not in teams:
                teams[team] = {'playValues': [], 'awardValues': [], 'totalValues': []}
            
            event = tba.team_events(team, year, False, True)[0]
            playPoints, awardPoints = slff.teamAtEvent(team, event)
            
            teams[team]['playValues'].append(playPoints)
            teams[team]['awardValues'].append(awardPoints)
            teams[team]['totalValues'].append(playPoints + awardPoints)
            
outData = []
for team in teams:
    avgPlay = stat.mean(teams[team]['playValues'])
    avgAward = stat.mean(teams[team]['awardValues'])
    avgTotal = stat.mean(teams[team]['totalValues'])
    
    maxPlay = max(teams[team]['playValues'])
    maxAward = max(teams[team]['awardValues'])
    maxTotal = max(teams[team]['totalValues'])
    
    teamObj = {'Team': team[3:],
               'Average Play': avgPlay,
               'Average Award': avgAward,
               'Average Total': avgTotal,
               'Max Play': maxPlay,
               'Max Award': maxAward,
               'Max Total': maxTotal}
               
    for idx, year in enumerate(range(currentYear - yearRange + 1, currentYear + 1)):
        teamObj[str(year) + ' Play'] = teams[team]['playValues'][idx]
        teamObj[str(year) + ' Award'] = teams[team]['awardValues'][idx]
        teamObj[str(year) + ' Total'] = teams[team]['totalValues'][idx]
    
    outData.append(teamObj)

colOrder = ['Team', 'Average Play', 'Average Award', 'Average Total', 'Max Play', 'Max Award', 'Max Total']
for year in range(currentYear - yearRange + 1, currentYear + 1):
    colOrder.append(str(year) + ' - Play')
    colOrder.append(str(year) + ' - Award')
    colOrder.append(str(year) + ' - Total')

gen.listOfDictToCSV("Worldwide Regional", outData, colOrder)