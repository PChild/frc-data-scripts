import pandas as pd
import tbapy

tba = tbapy.TBA('DJRE7IGB1IBTCtvpZfFnn7aZfBWoY9bTIZfQFY7CVBZ8tWeNRX6x0XdISQ63skHv')

YEAR = 2018

baseList = pd.read_csv('iriIN.csv')

#File to save out to, will overwrite if script is rerun.
f = open("iriEvents" + str(YEAR) + ".csv", 'w', encoding='utf-8')
f.write("team, events\n")

for team in baseList['teams']:
    print("Fetching team " + str(team))
    events = len(tba.team_events(int(team), YEAR, True, True))
    f.write(str(team) + ", " + str(events) + "\n")

f.close()