import tbapy

tba = tbapy.TBA('DJRE7IGB1IBTCtvpZfFnn7aZfBWoY9bTIZfQFY7CVBZ8tWeNRX6x0XdISQ63skHv')

safeTeams = {}
events = {}


safety = 18
winner = 1

print("Retrieving team data.")
for i in range(0,20):
    print("Fetching page " + str(i) + " of teams.")
    for team in tba.teams(i, 2018):
        for award in tba.team_awards(team['key']):
            
            safe = int(award['award_type'] is  safety)
            win = int(award['award_type'] is winner)
            
            if award['event_key'] in events:
                official = events[award['event_key']]
            else:
                print("Handling " + award['event_key'])
                eventType = tba.event(award['event_key'], True)['event_type']
                official = (eventType >= 0 and eventType < 99)
                events[award['event_key']] = official
         
            if official and (safe or win):
                if team['key'] in safeTeams:
                    safeTeams[team['key']]['win'] += win
                    safeTeams[team['key']]['safe'] += safe
                else:
                    safeTeams[team['key']] = {}
                    safeTeams[team['key']]['key'] = team['key']
                    safeTeams[team['key']]['win'] = win
                    safeTeams[team['key']]['safe'] = safe

print("Done fetching teams.")
print("Calculating safety scores.")

f = open("safetyFIRST.csv", 'w')
f.write("key, safety awards, wins, ratio \n")

for team in safeTeams:
    data = safeTeams[team]
    
    if data['win'] is 0:
        ratio = 10 * data['safe']
    elif data['safe'] is 0:
        ratio = -1 * data['win']
    else:
        ratio = data['safe'] / data['win'] 
        
    f.write(str(data['key']) + ", " + str(data['safe']) + ", " + str(data['win']) + ", " + str(ratio) + "\n")
    
f.close()