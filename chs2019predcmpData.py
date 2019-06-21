import gen
from tqdm import tqdm
import statistics as stat

tba = gen.setup()

teamList = ['frc540', 'frc1599', 'frc7886']

habLevels = ['None', 'HabLevel1', 'HabLevel2', 'HabLevel3']
outList = []

for team in tqdm(teamList):
    climbs = []
    starts = []
    lineCross = []
    matches = 0
    for match in tba.team_matches(team, None, 2019):
        try:
            matches += 1
            
            blueTeams = match['alliances']['blue']['team_keys']
            redTeams = match['alliances']['red']['team_keys']
            
            if team in blueTeams:
                slot = blueTeams.index(team) + 1
                color = 'blue'
            else:
                slot = redTeams.index(team) + 1
                color = 'red'
                
            climbs.append(habLevels.index(match['score_breakdown'][color]['endgameRobot'+str(slot)]))
            starts.append(habLevels.index(match['score_breakdown'][color]['preMatchLevelRobot'+str(slot)]))
            lineCross.append(match['score_breakdown'][color]['habLineRobot'+str(slot)] == 'CrossedHabLineInSandstorm')
        except:
            print('Match', match['key'], 'no work')
    outList.append({'Team': team,
                    'Avg Climb': stat.mean(climbs),
                    'Avg Start': stat.mean(starts),
                    'Max Start': max(starts),
                    'Line Cross': sum(lineCross) / matches})
    
gen.listOfDictToCSV('2019chcmpData', outList, ['Team', 'Avg Climb', 'Avg Start', 'Max Start', 'Line Cross'])