import gen

tba = gen.setup()
currentYear = 2018
years = range(1992, currentYear + 1)
#
#deansList = []
#for year in years:
#    events = tba.events(year)
#    
#    cmps = []
#    for event in events:
#        if event['event_type'] == 4:
#            cmps.append(event)
#    for event in cmps:
#        awards = tba.event_awards(event['key'])
#        
#        for award in awards:
#            if award['award_type'] == 4:
#                for kid in award['recipient_list']:
#                    deansList.append({'year': award['year'], 'team': kid['team_key'], 'awardee': kid['awardee']})
#                
#teams = {}
#for page in range(0, 16):
#    for team in tba.teams(page, currentYear):
#        teams[team['key']] = {'city': team['city'],
#                             'state': team['state_prov'],
#                             'country': team['country'], 
#                             'postal': team['postal_code'], 
#                             'name': team['nickname'], 
#                             'sponsors': team['name'].count('/') + 1}
#
#stateTeams = {}
#for key in teams:
#    state = teams[key]['state']
#    if state not in stateTeams:
#        stateTeams[state] = 1
#    else:
#        stateTeams[state] += 1
#
for student in deansList:
    studentTeam = tba.team(student['team'])
    student['city']  = studentTeam['city']
    student['country']  = studentTeam['country']    
    student['state']  = studentTeam['state_prov']
    student['name']  = studentTeam['nickname']
    student['postal']  = studentTeam['postal_code']
    student['sponsors'] = studentTeam['name'].count('/') + 1

for student in deansList:
    try:
        student['stateTeams'] = stateTeams[student['state']]
    except:
        student['stateTeams'] = ''
        
gen.listOfDictToCSV('deansList', deansList)