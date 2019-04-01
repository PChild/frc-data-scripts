import gen

tba = gen.setup()

dist = 'chs'
year = 2019

distKey = str(year)+dist
distEvents = tba.district_events(distKey, False, True)

oodPlays = []
for team in tba.district_teams(distKey, False, True):
    print("Processing team " + team)

    for event in tba.team_events(team, year, False):
        if event['key'] not in distEvents:
            teamModel = {'Team': team, 'Event': event['event_code'], 'Type': event['event_type']}
            oodPlays.append(teamModel)

gen.listOfDictToCSV(distKey +"_ood", oodPlays, ['Team', 'Event', 'Type'])