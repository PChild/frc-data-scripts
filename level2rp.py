import gen
from tqdm import tqdm

tba = gen.setup()

matchCount = 0
doubleL2 = 0
for event in tqdm(tba.events(2019)):
    for match in tba.event_matches(event['key']):
        if match['score_breakdown']:
            matchCount += 1
            for alliance in ['red', 'blue']:
                climbLevels = []
                data = match['score_breakdown'][alliance]
                for val in range(1,4):
                    climbLevels.append(data['endgameRobot' + str(val)])
                if climbLevels.count('HabLevel2') == 2 and climbLevels.count('HabLevel1') == 1:
                    doubleL2 += 1
        
print(doubleL2, "/", matchCount, "matches had no L3 climb but had RP")