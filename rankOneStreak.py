import gen

tba = gen.setup()

YEAR = 2018

def getRankOnes(year):
    rankOnes = []
    for event in tba.events(year, True, False):
        if event['event_type'] == 3:
            rankOnes += tba.event_alliances(event['key'])[0]['picks']
    return rankOnes

startTeams = getRankOnes(YEAR)
streakData = {}

for team in startTeams:
    streakData[team] = 1    

year = YEAR

while startTeams != []:
    year -= 1
    print("Processing", year)
    currentTeams = getRankOnes(year)
    
    tmpTeams = startTeams[:]
    for team in startTeams:
        if team not in currentTeams:
            tmpTeams.remove(team)
        else:
            streakData[team] += 1
        
    startTeams = tmpTeams[:]

f = open("rankOneStreaks.csv", "w")    
f.write("team, streak length \n")
for team in streakData:
    f.write(team + ", "+ str(streakData[team]) + "\n")
f.close()