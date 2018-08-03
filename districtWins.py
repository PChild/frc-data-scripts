import gen

tba = gen.setup()

dist = 'ont'
startYear = 2014
currYear = 2018

distTeams = tba.district_teams(str(currYear) + dist, False, True)

records = []
for team in distTeams:
    wins = 0
    for year in range(startYear, currYear + 1):
        awards = gen.readTeamCsv(team, 'awards', year)
        
        if awards is not None:
            for idx, award in awards.iterrows():
                if award['Type'] == 1:
                    wins += 1
    records.append({'Team': team[3:], 'Wins': wins})
    
records = sorted(records, key= lambda k: k['Wins'], reverse=True)
gen.listOfDictToCSV( dist.upper() + " " + str(startYear) + " to " + str(currYear) + " Wins", records, ['Team', 'Wins'])