import gen
import slff

currentYear = 2018
rookieYear = 2006

prevTeams = gen.readTeamListCsv(rookieYear - 1)['Teams']
currTeams = gen.readTeamListCsv(rookieYear)['Teams']

rookies = []
for team in currTeams:
    prevYears = slff.getTeamYears(team, rookieYear - 1)
    if len(prevYears) == 0:
        print(team)
        
        #Event data (ranks, opr)
        events = gen.readTeamCsv(team, 'events', currentYear)
        ranks = []
        oprs = []
        avgOpr = 0
        avgRank = 99
        if events is not None:
            for event in events['Event']:
                rank = gen.readEventCsv(event, 'rankings')
                opr = gen.readEventCsv(event, 'opr')
                
                if opr is not None:
                    oprs.append(opr[opr.Team == team]['OPR'].values[0])
                else:
                    print("Couldn't get OPR data for", event)
                if rank is not None:
                    if len(rank.columns) > 2:
                        rank = rank[['Rank', 'Team']]
                        if str(rank['Team'][0])[:3] != 'frc':
                            rank['Team'] = 'frc' + rank['Team'].astype(str)
                    rnk = rank[rank.Team == team]['Rank']
                    if len(rnk) > 0:
                        ranks.append(rnk.values[0])           
            if len(oprs) > 0:
                avgOpr = sum(oprs) / len(oprs)
            
            
            if len(ranks) > 0:
                avgRank = sum(ranks) / len(ranks)
        else:
            print("No 2018 events for", team)
        
        #Match data (wins, win %)
        matches = gen.readTeamCsv(team, 'matches', currentYear)
        wins = 0
        losses = 0
        ties = 0
        winPercent = 0
        if matches is not None:
            for idx, match in matches.iterrows():
                wins += gen.matchResult(team, match) == 'WIN'
                losses += gen.matchResult(team, match) == 'LOSS'
                ties += gen.matchResult(team, match) == 'TIE'
            
            if len(matches) > 0:
                winPercent = wins / sum([wins, losses, ties]) * 100
        
        
        awardCount = 0
        awardString = ""
        awards = gen.readTeamCsv(team, 'awards', currentYear)
        if awards is not None:
            awardCount = len(awards)
            
            for idx, award in awards.iterrows():
                tail = " / "
                
                if idx + 1 == len(awards):
                    tail = ""
                awardString += award['Name'] + tail 
        if winPercent > 0:    
            rookies.append({'Team': team,
                           '# of Awards': awardCount,
                           'Avg OPR': avgOpr,
                           'Avg Rank': avgRank,
                           'Wins': wins,
                           'Win %': winPercent,
                           'Awards': awardString})

colOrder = ['Team', 'Avg OPR', 'Avg Rank', 'Wins', 'Win %', '# of Awards', 'Awards']
gen.listOfDictToCSV("rookieData" + str(rookieYear), rookies, colOrder)                   
