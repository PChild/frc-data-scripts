import gen

tba = gen.setup()

chsTeams = tba.district_teams('2019chs', False, True)

teamData = []
for team in chsTeams:
    events = gen.readTeamCsv(team, 'events', 2018)
    seasonEvents = events[events.Type < 10]['Event']
    
    maxOPR = 0
    totalOPR = 0
    avgOPR = 0
    for event in events:
        eventData = gen.readEventCsv(event, 'opr')
        
        newOPR = eventData[eventData['Team'] == team]['OPR'].values[0]
        totalOPR += newOPR
        
        if maxOPR < newOPR:
            maxOPR = newOPR
            
    if len(events) != 0:    
        avgOPR = totalOPR / len(events)
    
    teamData.append({'Team': team[3:], 'Max OPR': maxOPR, 'Avg OPR': avgOPR})
    
gen.listOfDictToCSV('CHS Data 2018', teamData, ['Team', 'Max OPR', 'Avg OPR'])