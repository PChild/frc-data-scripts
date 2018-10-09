import gen

tba = gen.setup()
currentYear = 2019
startYear = 2016
district = 'chs'

years = range(startYear, currentYear)

yearData = {}

for year in years:
    yr = str(year)
    dist = yr + district
    yearData[yr] = {}
    yearData[yr]['Teams'] = tba.district_teams(dist, False, True)
    yearData[yr]['Points'] = {t['team_key']: t['point_total'] for t in tba.district_rankings(dist)}
    
currentTeams = tba.district_teams(str(currentYear) + district, False, True)

teamData = []
for team in currentTeams:
    events = gen.readTeamCsv(team, 'events', currentYear - 1)
    tm = tba.team(team)
    
    maxOPR = 0
    totalOPR = 0
    avgOPR = 0
    eventAdjust = 0
    
    if events is not None:
        seasonEvents = events[events.Type < 4]['Event']
        for event in seasonEvents:
            eventData = gen.readEventCsv(event, 'opr')
            
            teamRow = eventData[eventData['Team'] == team]
            if teamRow.empty:
                eventAdjust += 1
                newOPR = 0
            else:
                newOPR = teamRow['OPR'].values[0]
            
            totalOPR += newOPR
            
            if maxOPR < newOPR:
                maxOPR = newOPR
                
        if len(events) != 0:    
            avgOPR = totalOPR / (len(events) - eventAdjust)
    
    prevYearPoints = 0
    prevYear = str(currentYear - 1)
    if team in yearData[prevYear]['Teams']:
        prevYearPoints = yearData[prevYear]['Points'][team]
        
    totalPoints = 0
    yearsPlayed = 0
    for year in years:
        if team in yearData[str(year)]['Teams']:
            yearsPlayed += 1
            totalPoints += yearData[str(year)]['Points'][team]
    avgPoints = 0
    if yearsPlayed > 0:
        avgPoints = totalPoints / yearsPlayed 
    teamData.append({'Team': team[3:],
                     'Region': tm['state_prov'],
                     'Rookie Year': tm['rookie_year'],
                     'Max OPR': round(maxOPR, 2), 
                     'Avg OPR': round(avgOPR, 2), 
                     str(currentYear - 1) + ' Points': prevYearPoints,
                     'Avg Points': round(avgPoints, 2)})
    
teamData = sorted(teamData, key= lambda k: int(k['Team']))
gen.listOfDictToCSV(district.upper() + ' Data ' + str(currentYear - 1), teamData, ['Team', 'Region', 'Rookie Year', 'Avg Points', str(currentYear - 1) + ' Points', 'Max OPR', 'Avg OPR'])