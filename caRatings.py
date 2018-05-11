import tbapy

tba = tbapy.TBA('DJRE7IGB1IBTCtvpZfFnn7aZfBWoY9bTIZfQFY7CVBZ8tWeNRX6x0XdISQ63skHv')

teams2018 = tba.district_teams('2018chs', True)
chs_events = tba.district_events('2018chs', True)

winners = []

CURRENT_YEAR = 2018
CA_WEIGHT = 1
EI_WEIGHT = 0.5
ENT_WEIGHT = .25
CA = [0, 69, 51]
EI = [9]
ENT = [22]

for team in teams2018:
    
    print("Processing team " + team)
    
    teamRecord = {'team': team[3:], 'rating': 0, 'wins': ""} 
    
    for year in tba.team_years(team):
        
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
    winners.append(teamRecord)
    
f = open("chs_awards_2018.csv", 'w')
for winner in winners:
    f.write(str(winner['team']) + ", " + str(winner['rating']) + ", " + str(winner['wins']) + "\n")
f.close()