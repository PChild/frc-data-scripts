import gen
import pandas

tba = gen.setup()

draftData = pandas.read_excel('currentDrafts.xlsx')
draftData = draftData.dropna(how='all')
draftData = draftData.fillna(-1)

missingList = []
for idx, event in draftData.iterrows():
    if "!" in event['Code']:
        eventTeams = tba.district_teams(str(2019) + event['Code'].strip('!').lower(), False, True)
    else:
        eventTeams = tba.event_teams(event['Code'], False, True)
    
    for num in range(1, 13):
        val = 'Pick ' + str(num)
        team = str(int(event[val]))
        
        if not team == '-1':
            if 'frc' +  team not in eventTeams:
                missingList.append({'Event': event['Code'], 'Team': team})
                print(team, 'is missing from', event['Code'])

if len(missingList) > 0:
    gen.listOfDictToCSV('missingTeams2019', missingList, ['Event', 'Team'])
else:
    print('No teams missing!')