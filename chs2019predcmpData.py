import gen
from tqdm import tqdm
import statistics as stat

tba = gen.setup()

teamList = ['frc339', 'frc346', 'frc384', 'frc401', 'frc422', 'frc449', 'frc539',
            'frc612', 'frc614', 'frc619', 'frc686', 'frc836', 'frc888', 'frc977',
            'frc1086', 'frc1111', 'frc1123', 'frc1262', 'frc1413', 'frc1418',
            'frc1610', 'frc1629', 'frc1719', 'frc1727', 'frc1731', 'frc1885',
            'frc2068', 'frc2106', 'frc2199', 'frc2363', 'frc2534', 'frc2537',
            'frc2849', 'frc2912', 'frc2914', 'frc2998', 'frc3274', 'frc3359',
            'frc3748', 'frc3793', 'frc4099', 'frc4242', 'frc4456', 'frc4472',
            'frc4541', 'frc4638', 'frc5338', 'frc5546', 'frc5587', 'frc5830',
            'frc6334', 'frc6543', 'frc6802', 'frc6882', 'frc7770']

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