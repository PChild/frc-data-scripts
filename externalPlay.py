# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 14:35:23 2017

@author: pchild
"""

import tbapy

tba = tbapy.TBA('DJRE7IGB1IBTCtvpZfFnn7aZfBWoY9bTIZfQFY7CVBZ8tWeNRX6x0XdISQ63skHv')

teams2018 = tba.district_teams('2018chs', True)
chs_events = tba.district_events('2018chs', True)

oodPlays = []

for team in teams2018:
    print("Processing team " + team)
    events = tba.team_events(team, 2018, False)
    
    for event in events:
        if event['key'] not in chs_events:
            teamModel = {'team': team, 'event': event['event_code'], 'type': event['event_type']}
            oodPlays.append(teamModel)

f = open("chs_ood_2018.csv", 'w')
for ood in oodPlays:
    f.write(str(ood['team']) + ", " + str(ood['event']) + ", " + str(ood['type']) + "\n")
f.close()