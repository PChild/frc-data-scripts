import gen

tba = gen.setup()

YEAR = 2018
DISTRICT = 'chs'
DCMP_EVENTS = [2, 5]

pointsData = []

districtTeams = tba.district_teams(str(YEAR) + DISTRICT, False, False)
teamCount = len(districtTeams)

print("Processing", teamCount , "district teams.")

teamIter = 0
for team in districtTeams:
    teamIter += 1
    gen.progressBar(teamIter, teamCount)    
    
    distPoints = 0
    teamEvents = tba.team_events(team['key'], YEAR, True, False)
    
    teamEvents = sorted(teamEvents, key = lambda k: k['start_date'])
    
    try:
        for i in range(0,3):
            eventPoints = tba.event_district_points(teamEvents[i]['key'])
            distPoints += eventPoints['points'][team['key']]['total']
    except:
        pass
    pointsData.append({'team': team['team_number'], 'points': distPoints})

gen.listOfDictToCSV(DISTRICT + str(YEAR) + "points", pointsData)