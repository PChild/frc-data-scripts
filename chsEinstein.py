import gen
import eventTypes

tba = gen.setup()

chsTeams = tba.district_teams('2019chs', False, True)

onEinstein = []

for year in range(1992, 2019):
    for event in tba.events(year):
        if event['event_type'] == eventTypes.CMP_FINALS:
            for team in tba.event_teams(event['key'], False, True):
                if team in chsTeams:
                    matches = tba.team_matches(team, event['key'])
                    if len(matches) > 0:
                        onEinstein.append([team, year])
                    
print(onEinstein)

