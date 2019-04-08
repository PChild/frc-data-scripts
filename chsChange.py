import tbapy
tba = tbapy.TBA('DJRE7IGB1IBTCtvpZfFnn7aZfBWoY9bTIZfQFY7CVBZ8tWeNRX6x0XdISQ63skHv')

teams2017 = tba.district_teams('2017chs', True, True)
teams2018 = tba.district_teams('2018chs', True, True)

for team in teams2017:
    if team not in teams2018:
        print("Lost " + team)
        
for team in teams2018:
    if team not in teams2017:
        print("Gained " + team)