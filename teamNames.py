import gen
import pandas as pd
from tqdm import tqdm

tba = gen.setup()
teamDf = pd.read_csv('rawTeams.csv', header=None, index_col=0)
teams2019 = gen.readTeamListCsv(2019)['Teams']

names = []
for team in tqdm(teams2019):
    if team in teamDf.index:
        names.append({'Team': team[3:], 'Name': teamDf.loc[team][1]})
    else:
        names.append({'Team': team[3:], 'Name': tba.team(team)['nickname']})
        
gen.listOfDictToCSV('Team Names', names, ['Team', 'Name'])