import gen

teams = gen.readTeamListCsv(2018)['Teams']

records = []
for team in teams:
    matches = gen.readTeamCsv(team, 'matches', 2018)
    
    wins = 0
    losses = 0
    ties = 0
    
    if matches is not None:
        for idx, match in matches.iterrows():
            result = gen.matchResult(team, match)
            
            wins += result == 'WIN'
            losses += result == 'LOSS'
            ties += result == 'TIE'
            
        total = wins + losses + ties
        if total != 0:
            if wins == 0:
                wins = 1
                total = total * 10
                rating = wins / total
                wins = 0
            else:
                rating = wins / total
            recordString = str(wins) + ' / ' + str(losses) + ' / ' + str(ties)
            records.append({'Team': team[3:],
                            'Rating': rating,
                            'Record': recordString})

records = sorted(records, key= lambda k:k['Rating'])
gen.listOfDictToCSV('Worst Records', records, ['Team', 'Rating', 'Record'])