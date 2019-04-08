import tbapy

tba = tbapy.TBA('DJRE7IGB1IBTCtvpZfFnn7aZfBWoY9bTIZfQFY7CVBZ8tWeNRX6x0XdISQ63skHv')

teams2017 = tba.district_teams('2017chs', True)
chs_events = tba.district_events('2017chs', True)

winners = {}

CURRENT_YEAR = 2017
CA_WEIGHT = 1
EI_WEIGHT = 0.5
ENT_WEIGHT = .25
CA = [0, 69, 51]
EI = [9]
ENT = [22]

for team in teams2017:
    
    print("Processing team " + team)
    
    teamRecord = {'team': team[3:], 'rating': 0, 'wins': ""} 
    
    for year in tba.team_years(team):
        if year < CURRENT_YEAR:
            print("Processing year " + str(year))
            caCount = 0
            eiCount = 0
            entCount = 0
            
            teamAwards = tba.team_awards(team, year)
            
            for award in teamAwards:
                
                awardString = award['name'] + " at " + award['event_key'] + ", "
                
                if award['award_type'] in CA:
                    caCount += 1
                    teamRecord['wins'] += awardString
                elif award['award_type'] in EI:
                    eiCount += 1
                    teamRecord['wins'] += awardString
                elif award['award_type'] in ENT:
                    entCount += 1
                    teamRecord['wins'] += awardString
            
            teamRecord['rating'] += (caCount * CA_WEIGHT + eiCount * EI_WEIGHT + entCount * ENT_WEIGHT) / (CURRENT_YEAR - year + 1)
    winners[str(team[3:])] = teamRecord

for event in chs_events:
    print('Processing ' + event)
    eventRatings = []
    eventAwards = tba.event_awards(event)
    awardsRecords = []
    
    eventFileName = str(event) + '_results.csv'
    f = open(eventFileName, 'w')
    
    teamList = tba.event_teams(event, True)
    teamList = [t.strip('frc') for t in teamList]
    
    for team in teamList:
        try:
            teamRating = winners[str(team)]['rating']
        except:
            teamRating = 0
        record = {'team': team, 'rating': teamRating}
        f.write(str(record['team']) + ", " + str(record['rating']) + '\n')
    for award in eventAwards:
        try:
            winner = award['recipient_list'][0]['team_key'][3:]
        except:
            winner = award['recipient_list'][0]['awardee']
        record = {'team': winner, 'name': award['name']}
        f.write(str(record['team']) + ", " + str(record['name']) + '\n')
    f.close()
    
f = open("chs_ratings_2017.csv", 'w')
for team in winners:
    f.write(str(winners[str(team)]['team']) + ", " + str(winners[str(team)]['rating']) + ", " + str(winners[str(team)]['wins']) + "\n")
f.close()