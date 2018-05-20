import pandas as pd
import tbapy

tba = tbapy.TBA('DJRE7IGB1IBTCtvpZfFnn7aZfBWoY9bTIZfQFY7CVBZ8tWeNRX6x0XdISQ63skHv')

YEAR = 2018

baseList = pd.read_csv('iriIN.csv')

#only count regionals, districts, dcmp, and worlds
normalEvents = range(0,6)

f = open("iriEvents" + str(YEAR) + ".csv", 'w', encoding='utf-8')
f.write("team, events, wins, finalist\n")

for team in baseList['teams']:
    print("Fetching team " + str(team))
    
    eventCount = 0
    winCount = 0
    finalistCount = 0
    for award in tba.team_awards(int(team), YEAR):
        winCount += award['award_type'] == 1
        finalistCount += award['award_type'] == 2
    for event in tba.team_events(int(team), YEAR, True, False):
        if event['event_type'] in normalEvents:
            eventCount += 1        
    f.write(str(team) + ", " + str(eventCount) + ", " + str(winCount) + ", " + str(finalistCount) + "\n")

f.close()