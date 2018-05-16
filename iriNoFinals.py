import tbapy

tba = tbapy.TBA('DJRE7IGB1IBTCtvpZfFnn7aZfBWoY9bTIZfQFY7CVBZ8tWeNRX6x0XdISQ63skHv')

noFinals = []

for year in range(2012, 2018):
    print("Processing " + str(year))
    teams = tba.event_teams(str(year)+"iri", True, True)
    
    for team in teams:
        awards = tba.team_awards(team, year)

        madeFinals = False        
        
        for award in awards:
            madeFinals = madeFinals or award['award_type'] in [1,2]
        
        if not madeFinals:
            print("Team " + str(team[3:]) + " missed finals in " + str(year))
            noFinals.append({'team': team[3:], 'year': year})

f = open("iriNoFinals.csv", 'w', encoding='utf-8')

for team in noFinals:
    for prop in team.keys():
        f.write(str(team[prop]) + ", ")
    f.write("\n")
f.close()