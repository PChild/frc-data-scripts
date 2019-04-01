import gen

tba = gen.setup()

YEAR = 2019
DISTRICT = 'chs'

teams = tba.district_teams(str(YEAR - 1) + DISTRICT, True, True)

winners = []

CA_WEIGHT = 1
EI_WEIGHT = 0.5
ENT_WEIGHT = .25
CA = [0, 69, 51]
EI = [9]
ENT = [22]

for team in teams:
    
    print("Processing team " + team)
    
    teamRecord = {'team': team[3:], 'rating': 0, 'wins': ""}
    
    teamAwards = tba.team_awards(team)
    
    for year in range(1992, YEAR):
        caCount = 0
        eiCount = 0
        entCount = 0
        gotAward = False

        for award in teamAwards:
            if award['year'] == year:            
                awardString = award['event_key'] + " / "
                
                if award['award_type'] in CA:
                    gotAward = True
                    caCount += 1
                    teamRecord['wins'] = "CA at " + awardString + teamRecord['wins']
                elif award['award_type'] in EI:
                    gotAward = True
                    eiCount += 1
                    teamRecord['wins'] = "EI at " + awardString + teamRecord['wins']
                elif award['award_type'] in ENT:
                    gotAward = True
                    entCount += 1
                    teamRecord['wins'] = "ENT at " + awardString + teamRecord['wins']
        if gotAward:
            print("Award in " + str(year))
            teamRecord['rating'] += (caCount * CA_WEIGHT + eiCount * EI_WEIGHT + entCount * ENT_WEIGHT) / (YEAR - year + 1)
    winners.append(teamRecord)

gen.listOfDictToCSV(DISTRICT.upper() +"caRatings", winners)