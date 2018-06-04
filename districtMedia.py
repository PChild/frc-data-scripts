import gen

tba = gen.setup()

YEAR = 2018
DISTRICT = 'chs'

distTeams = []
teamList = tba.district_teams(str(YEAR) + DISTRICT)

for index, team in enumerate(teamList):
    gen.progressBar(index, len(teamList))
    distTeams.append({'team': team['team_number'], 'name': team['nickname'], 'website': team['website'], 'facebook': "", 'github': "", 'twitter': "", 'instagram': "", 'youtube': ""})
    
    for site in tba.team_profiles(team['team_number']):
        siteType = site['type'][:-8]
        distTeams[index][siteType] = "www." + siteType + ".com/" + site['foreign_key']

gen.listOfDictToCSV(DISTRICT + str(YEAR) + "profiles", distTeams)