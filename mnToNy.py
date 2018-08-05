import gen

tba = gen.setup()

mnTeams = []
for page in range(0, 16):
    teams = tba.teams(page)    
    if len(teams) == 0:
        break    
    for team in  teams:
        if team['state_prov'] in ['MN', 'Minnesota']:
            if team['key'] not in mnTeams:
                mnTeams.append(team['key'])
print('Found', str(len(mnTeams)), 'MN teams.')

mnInNyEvents = []
for year in range(1992, 2019):
    nyEvents = 0
    for event in tba.events(year):
        if event['state_prov'] in ['NY', 'New York']:
            nyEvents += 1
            for team in tba.event_teams(event['key'], False, True):
                if team in mnTeams:
                    mnInNyEvents.append({'Team': team, 'Event': event['key']})
    print('There were', str(nyEvents), 'NY events in', str(year))
print('From 1992 to 2018', str(len(mnInNyEvents)), 'MN teams went to NY events.')
if len(mnInNyEvents) > 0:
    gen.listOfDictToCSV('Minnesota teams in New York', mnInNyEvents)