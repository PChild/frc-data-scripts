import gen

tba = gen.setup()

EVENT = "2018txri"

teams = tba.event_teams(EVENT, False, True)

elimMatches = []
for match in tba.event_matches(EVENT, True):
    if match['comp_level'] != 'qm':
        elimMatches.append(match)

data = []
for idx, team in enumerate(teams):
    gen.progressBar(idx, len(teams))
    status = tba.team_status(team, EVENT)
    
    record = status['qual']['ranking']['record']
    qualPoints = record['wins'] * 3 + record['ties']
    
    rank = status['qual']['ranking']['rank']
    
    if rank == 1:
        rankPoints = 12
    elif rank < 4:
        rankPoints = 8
    elif rank < 9:
        rankPoints = 5
    elif rank < 13:
        rankPoints = 3
    elif rank < 17:
        rankPoints = 2
    elif rank < 21:
        rankPoints = 1
    else:
        rankPoints = 0
    
    elimPoints = 0    
    elims = status['playoff']
    if elims:
        if elims['level'] == 'f':
            if elims['status'] == 'won':
                elimPoints = 27
            else:
                elimPoints = 20
                if elims['current_level_record']['wins'] > 0:
                    elimPoints += 4
        elif elims['level'] == 'sf':
            elimPoints = 10
            if elims['current_level_record']['wins'] > 0:
                elimPoints += 2
        elif elims['level'] == 'qf':
            elimPoints = 4
            if elims['current_level_record']['wins'] > 0:
                elimPoints += 1
        
        inMatch = 0
        for match in elimMatches:
            inMatch += team in match['alliances']['blue']['team_keys']
            inMatch += team in match['alliances']['red']['team_keys']
    
        rec = status['playoff']['record']
        backup = inMatch / (rec['wins'] + rec['losses'] + rec['ties']) + 0.5
        
        scales = [1.05, 1.0, 0.95, backup]
        position = status['alliance']['pick']
        
        scaleFactor = max([scales[position], .25])

    total = (elimPoints + qualPoints + rankPoints) * scaleFactor
    
    data.append({'team': team[3:], 'rank': rank, 'quals': qualPoints, 'rankP': rankPoints, 'elims': elimPoints, 'total': total, 'factor': scales[position]})

colOrder = ['team', 'rank', 'total', 'factor', 'rankP', 'quals', 'elims']    
gen.listOfDictToCSV(EVENT+'FFIT', data, colOrder)