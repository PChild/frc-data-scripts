import gen
import pandas as pd
from tqdm import tqdm

tba = gen.setup()
cols = ['Key', 'Team']
waiver1 = pd.read_csv('Waiver1Teams.csv')
waiver1.columns = cols
draftData = pd.read_excel('Waiver Lists.xlsx')

waiver2 = pd.read_csv('Waiver2Teams.csv')
waiver2.columns = cols

waiverTeams = []
for col in tqdm(draftData.columns):
    draftData[col] = draftData[col].fillna(-1).astype(int).astype(str)
    key = col
    baseTeams = []
    
    if "!" in key:
        pass
        #Skipping districts for now.
        #key = key.strip("!")
        #baseTeams = tba.district_teams(str(2019)+key.lower(), False, True)
    else:
        baseTeams = tba.event_teams(key, False, True)
        
    currentTeams = [team[3:] for team in baseTeams]    
    for team in currentTeams:
        if not draftData[col].str.contains(team).any():
            if int(team) not in waiver1['Team'].values or int(team) not in waiver2['Team'].values:
                waiverTeams.append({'Key': key, 'Team': team})
   
newTeams = len(waiverTeams)      
print(newTeams, 'new teams found for waivers.')
if newTeams > 0:
    gen.listOfDictToCSV('Waiver3Teams', waiverTeams, cols)