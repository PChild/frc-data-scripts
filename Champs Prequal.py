import gen

tba = gen.setup()
prevYear = 2018

HoF = [16, 23, 27, 51, 67, 103, 111, 120, 175, 236, 254, 341, 359, 365, 597, 842, 987, 1114, 1538, 2614, 3132, 2834, 1311]
OaS = [20, 45, 126, 148, 151, 157, 191, 190, 250]

preQual = HoF[:]
for team in OaS:
    if team not in preQual:
        preQual.append(team)

finals = []
divisions = []
for event in tba.events(prevYear):
    typ = event['event_type'] 
    if  typ == 3:
        divisions.append(event['key'])
    if typ == 4:
        finals.append(event['key'])

for event in finals:
    awards = tba.event_awards(event)
    
    for award in awards:
        typ = award['award_type']
        if  typ == 0 or typ == 1 or typ == 69:
            for team in award['recipient_list']:
                teamVal = int(team['team_key'][3:])
                if teamVal not in preQual:
                    preQual.append(teamVal)
        
for event in divisions:
    awards = tba.event_awards(event)
    
    for award in awards:
        typ = award['award_type'] 
        if  typ == 9:
            for team in award['recipient_list']:
                teamVal = int(team['team_key'][3:])
                if teamVal not in preQual:
                    preQual.append(teamVal)

champsData = []
for team in preQual:
    info = tba.team(team)
    champsData.append({'Team': team, 'Champs': info['home_championship']['2018']})
    

detCount = 0
for team in champsData:
    detCount += team['Champs'] == 'Detroit'

print(detCount, "/", len(champsData), "Detroit teams")
gen.listOfDictToCSV('Prequalified Champs Data', champsData, ['Team', 'Champs'])