import gen
import math
from scipy.special import erfinv
import statistics as stat

yearRange = 4
currentYear = 2018

years = range(currentYear - yearRange + 1, currentYear + 1)

def teamAtEvent(team, event):
    ROBOT_AWARDS = [16, 17, 20, 21, 29, 71]
    OTHER_AWARDS = [1, 2, 5, 11, 13, 14, 18, 22, 27, 30]
    CA = 0
    EI = 9
    WF = 3
    DEANS = 4
    RAS = 10
    RI = 15
    CAF = 69
    WILDCARD = 68
    
    awardData = {'REG': {CA: 60, EI: 45, RAS: 25, RI: 15, WF: 10, DEANS: 5, WILDCARD: 0, 'ROBOT': 20, 'OTHER': 5},
                 'CMP': {CA: 110, EI: 60, RAS: 35, RI: 20, WF: 30, DEANS: 15, CAF: 90, 'ROBOT': 30, 'OTHER': 10}}
                 
    #Fetch event info, do this first since we only want to really process official events.             
    eventInfo = gen.readTbaCsv(event, 'info')
    isOfficial = eventInfo['Type'][0] in range(0, 7)
    isChamps = eventInfo['Type'][0] in range(3, 5)

    awardPoints = 0
    playPoints = 0
    
    if isOfficial:
        eventType = 'CMP' if isChamps else 'REG'
        
        tya = gen.readTbaCsv(team, 'awards', True, event[:4])
        teamEventAwards = tya[tya.Event == event]
        playPoints = calcPoints(team, event)
        
        for idx, row in teamEventAwards.iterrow():
            awardType = row['Type']
            
            if awardType in ROBOT_AWARDS:
                awardType = 'ROBOT'
            if awardType in OTHER_AWARDS:
                awardType = 'OTHER'
            awardPoints += awardData[eventType][awardType]
            
    return [playPoints, awardPoints]

def calcPoints(team, event):
    draftPoints = 0
    rankPoints = 0
    elimPoints = 0
     
    eM = gen.readTbaCsv(event, 'matches', names=['key', 'r1', 'r2', 'r3', 'b1', 'b2', 'b3', 'rScore', 'bScore'])
    teamMatches = eM[(eM.r1 == team) | (eM.r2 == team) | (eM.r3 == team) | (eM.b1 == team) | (eM.b2 == team) | (eM.b3 == team)]
    
    rK = gen.readTbaCsv(event, 'rankings')
    teamRank = rK[rK.Team == team]['Rank'].iloc[0]
    teamCount = len(rK)
    
    alpha = 1.07
    rankPoints = math.ceil(abs(erfinv( (teamCount - 2 * teamRank + 2) /  (alpha * teamCount)) * 10 / erfinv( 1 / alpha ) + 12 ))
    
    aL = gen.readTbaCsv(event, 'alliances', names=['captain', 'firstPick', 'secondPick'])
    aLL = aL[(aL.captain == team) | (aL.firstPick == team) | (aL.secondPick == team)]
    
    if len(aLL) > 0:
        alliance = {'pick': 9, 'number': 9}
        alliance['number'] = aLL.index.values[0]
        
        if aLL['captain'] == team:
            alliance['pick'] = 0
        elif aLL['firstPick'] == team:
            alliance['pick'] = 1
        elif aLL['secondPick'] == team:
            alliance['pick'] = 2

        if alliance['pick'] < 2:
            draftPoints = 17 - alliance['number']
        elif alliance['pick'] == 2:
            draftPoints = alliance['number']

    #Find points for playing in elims
    for idx, match in teamMatches.iterrows():
        if match['key'].split('_')[1][:2] != 'qm':
            onRed = (match['r1'] == team) or (match['r2'] == team) or (match['r3'] == team)
            onBlue = not onRed
            redWins = match['rScore'] > match['bScore']
            blueWins = match['bScore'] > match['rScore']
            
            if (onRed and redWins) or (onBlue and blueWins):
                elimPoints += 5
    
    return draftPoints + rankPoints + elimPoints

teams = {}
for idx, year in enumerate(range(currentYear - yearRange + 1, currentYear + 1)):
    gen.progressBar(idx, currentYear + 1)
    
    for i in range(0,20):
        for team in tba.teams(i, year, False, True):
            if team not in teams:
                teams[team] = {'playValues': [], 'awardValues': [], 'totalValues': []}
            
            event = tba.team_events(team, year, False, True)[0]
            playPoints, awardPoints = teamAtEvent(team, event)
            
            teams[team]['playValues'].append(playPoints)
            teams[team]['awardValues'].append(awardPoints)
            teams[team]['totalValues'].append(playPoints + awardPoints)
            
outData = []
for team in teams:
    avgPlay = stat.mean(teams[team]['playValues'])
    avgAward = stat.mean(teams[team]['awardValues'])
    avgTotal = stat.mean(teams[team]['totalValues'])
    
    maxPlay = max(teams[team]['playValues'])
    maxAward = max(teams[team]['awardValues'])
    maxTotal = max(teams[team]['totalValues'])
    
    teamObj = {'Team': team[3:],
               'Average Play': avgPlay,
               'Average Award': avgAward,
               'Average Total': avgTotal,
               'Max Play': maxPlay,
               'Max Award': maxAward,
               'Max Total': maxTotal}
               
    for idx, year in enumerate(range(currentYear - yearRange + 1, currentYear + 1)):
        teamObj[str(year) + ' Play'] = teams[team]['playValues'][idx]
        teamObj[str(year) + ' Award'] = teams[team]['awardValues'][idx]
        teamObj[str(year) + ' Total'] = teams[team]['totalValues'][idx]
    
    outData.append(teamObj)

colOrder = ['Team', 'Average Play', 'Average Award', 'Average Total', 'Max Play', 'Max Award', 'Max Total']
for year in range(currentYear - yearRange + 1, currentYear + 1):
    colOrder.append(str(year) + ' - Play')
    colOrder.append(str(year) + ' - Award')
    colOrder.append(str(year) + ' - Total')

gen.listOfDictToCSV("Worldwide Regional", outData, colOrder)