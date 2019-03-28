import gen
import eventTypes
import slffFunctions
from tqdm import tqdm

tba = gen.setup()

dist = 'ont'
year = 2018

dcmpTypes = [eventTypes.DISTRICT_CMP, eventTypes.DISTRICT_CMP_DIVISION]

print('Fetching district events')
distEvents = tba.district_events(str(year) + dist)
dcmpEvents = [event for event in distEvents if event['event_type'] in dcmpTypes]

print('Fetching DCMP / divisions teams')
dcmpTeams = []
for event in dcmpEvents:
    dcmpTeams += tba.event_teams(event['key'], False, True)

dcmpTeams = list(set(dcmpTeams))

print('Processing team performances')
for team in tqdm(dcmpTeams):
    teamEvents = tba.team_events(team, year)
    
    teamData = {'plays': [], 'awards': []}
    
    for event in teamEvents:
        if event['event_type'] not in dcmpTypes:
            teamData['plays'].append(slffFunctions.getPlayPoints(team, event['key']))
            teamData['awards'].append(slffFunctions.getAwardPoints(team, event['key']))
            