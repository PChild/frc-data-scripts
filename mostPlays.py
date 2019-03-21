import gen
import pandas as pd
from tqdm import tqdm

tba = gen.setup()

matchData = []

teamList = gen.readTeamListCsv(2018)['Teams'].tolist()

for team in tqdm(teamList):
    teamMax = 0
    yearMax = 0
    
    for year in range(2008, 2019):
        matchesPlayed = len(tba.team_matches(team, None, year, False, True))
        
        if matchesPlayed > teamMax:
            teamMax = matchesPlayed
            yearMax = year
    
    matchData.append({'Team': team, 'Max Matches': teamMax, 'Year': year})
    
matchDf = pd.DataFrame(matchData).sort_values('Max Matches').to_csv('TeamMaxMatches.csv', index=False)