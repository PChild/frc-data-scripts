# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 14:07:28 2017

@author: pchild
"""

import tbapy
import csv

tba = tbapy.TBA('DJRE7IGB1IBTCtvpZfFnn7aZfBWoY9bTIZfQFY7CVBZ8tWeNRX6x0XdISQ63skHv')
awards = []
  
with open('teams.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    teams = list(reader)

f = open("chs_awards.csv", 'w')

def getTeamAwards(team):
    print("Getting awards for team " + str(team))
    rawAwards = tba.team_awards(team)
    
    for award in rawAwards:
        if award['award_type'] == 1:
            f.write(str(team[3:]) + ", " + str(award['event_key'])[:4] + ", " + award['event_key'][4:] + ", " + award['name'] + "\n")

for team in teams:
    getTeamAwards(team[0])

f.close()