import gen

tba = gen.setup()

desiredRegion = ['Virginia', 'Maryland', 'District of Columbia']
regionKey = 'CHS'

champsPicks = []
for year in range(2012, 2019):
    teamList = []
    for event in tba.events(year):
        if event['event_type'] == 3:
            for alliance in tba.event_alliances(event['key']):
                for team in alliance['picks']:
                    if tba.team(team)['state_prov'] in desiredRegion:
                         teamList.append(team[3:])
    champsPicks.append({'Year': year, 'Count': len(teamList), 'Teams': ' '.join(teamList)})
gen.listOfDictToCSV(regionKey + ' Champs Picks', champsPicks, ['Year', 'Count', 'Teams'])