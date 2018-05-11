import tbapy
import string
printable = set(string.printable)

tba = tbapy.TBA('DJRE7IGB1IBTCtvpZfFnn7aZfBWoY9bTIZfQFY7CVBZ8tWeNRX6x0XdISQ63skHv')

f = open("chs2018.csv", 'w')

EVENT = '2018chcmp'
chs2018 = tba.district_teams('2018chs')
dcmp2018 = tba.event_teams(EVENT)

chsTeams = []
dcmpTeams = []
    
for team in dcmp2018:
    dcmpTeams.append(team['team_number'])

fields = ['team_number',
          'postal_code',
          'state_prov',
          'rookie_year',
          'dcmp'
          ]

for t in chs2018:
    t['dcmp'] = "false"
    if t['team_number'] in dcmpTeams:
        t['dcmp'] = "true"
    for i in fields:
        f.write(str(t[i]) + ", ")
    f.write("\n")
f.close()