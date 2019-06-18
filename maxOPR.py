import gen
import eventTypes

tba = gen.setup()

teams = [48, 117, 120, 144, 156, 291, 337, 379, 1708, 1787, 2399, 2641, 3138,
         3266, 3324, 3484, 3504, 4027, 4028, 4085, 4145, 4150, 4269, 5413,
         5667, 5811, 6936, 7165, 7274, 7486, 7515, 7670]

year = 2019
eventKey = 'wow'

oprs = []
for team in teams:
    rankingPts = []
    maxOPR = 0
    for event in tba.team_events(team, year):
        if event['event_type'] in [eventTypes.CMP_DIVISION, eventTypes.DISTRICT, eventTypes.DISTRICT_CMP_DIVISION, eventTypes.REGIONAL]:
            currOPR = tba.event_oprs(event['key'])['oprs']['frc'+str(team)]
            
            teamRP = [item['extra_stats'][0] for item in tba.event_rankings(event['key'])['rankings'] if item['team_key'] == 'frc'+str(team)][0]
            
            rankingPts.append(teamRP)
            if currOPR > maxOPR:
                maxOPR = currOPR
    oprs.append({'team': team, 'opr': maxOPR, 'avgRP': sum(rankingPts) / len(rankingPts)})
    
gen.listOfDictToCSV(str(year) + eventKey + ' Data', oprs, ['team', 'opr', 'avgRP'])