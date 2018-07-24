from scipy.special import erfinv
from multiprocessing import Pool
from functools import partial
import statistics as stat
import math
import gen

yearRange = 3
currentYear = 2018
years = range(currentYear - yearRange + 1, currentYear + 1)

teams = {}

def teamAtEvent(team, event):
    ROBOT_AWARDS = [16, 17, 20, 21, 29, 71]
    OTHER_AWARDS = [ 5, 11, 13, 14, 18, 22, 27, 30]
    NO_POINTS = [1, 2]
    CA = 0
    EI = 9
    WF = 3
    DEANS = 4
    RAS = 10
    RI = 15
    CAF = 69
    WILDCARD = 68
    
    awardData = {'REG': {CA: 25, EI: 15, RAS: 5, RI: 5, WF: 5, DEANS: 5, WILDCARD: 0, 'ROBOT': 10, 'OTHER': 5, 'NONE': 0},
                 'CMP': {CA: 110, EI: 60, RAS: 35, RI: 20, WF: 30, DEANS: 15, CAF: 90, 'ROBOT': 30, 'OTHER': 10, 'NONE': 0}}
    
    awardPoints = 0
    playPoints = 0
    #Fetch event info, do this first since we only want to really process official events.             
    eventInfo = gen.readEventCsv(event, 'info')
    
    if eventInfo is not None:
        isOfficial = eventInfo['Type'][0] in range(0, 7)
        isChamps = eventInfo['Type'][0] in range(3, 5)
        eventType = 'CMP' if isChamps else 'REG'      
            
        if isOfficial:
            playPoints = calcPoints(team, event)
                  
            tya = gen.readTeamCsv(team, 'awards', event[:4])
                        
            if tya is not None:
                teamEventAwards = tya[tya.Event == event]
                
                for idx, row in teamEventAwards.iterrows():
                    awardType = row['Type']
                    
                    if awardType in ROBOT_AWARDS:
                        awardType = 'ROBOT'
                    if awardType in OTHER_AWARDS:
                        awardType = 'OTHER'
                    if awardType in NO_POINTS:
                        awardType = 'NONE'
                    awardPoints += awardData[eventType][awardType]
            
    return [playPoints, awardPoints]

def calcPoints(team, event):
    draftPoints = 0
    rankPoints = 0
    elimPoints = 0
     
    eM = gen.readEventCsv(event, 'matches', names=['key', 'r1', 'r2', 'r3', 'b1', 'b2', 'b3', 'rScore', 'bScore'])
    teamMatches = eM[(eM.r1 == team) | (eM.r2 == team) | (eM.r3 == team) | (eM.b1 == team) | (eM.b2 == team) | (eM.b3 == team)]
    
    rK = gen.readEventCsv(event, 'rankings')
    tmpRk = rK[rK.Team == team]
    
    if len(tmpRk) > 0:
        teamRank = rK[rK.Team == team]['Rank'].iloc[0]
        teamCount = len(rK)
        
        alpha = 1.07
        rankPoints = math.ceil(abs(erfinv( (teamCount - 2 * teamRank + 2) /  (alpha * teamCount)) * 10 / erfinv( 1 / alpha ) + 12 ))
    
    aL = gen.readEventCsv(event, 'alliances', names=['captain', 'firstPick', 'secondPick'])
    aLL = aL[(aL.captain == team) | (aL.firstPick == team) | (aL.secondPick == team)]
    
    if len(aLL) > 0:
        alliance = {'pick': 9, 'number': 9}
        alliance['number'] = aLL.index.values[0]
        
        if aLL['captain'].values[0] == team:
            alliance['pick'] = 0
        elif aLL['firstPick'].values[0] == team:
            alliance['pick'] = 1
        elif aLL['secondPick'].values[0] == team:
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

def getData(year, team):
    playPoints = 0
    awardPoints = 0
    
    teamEvents = gen.readTeamCsv(team, 'events', year)    
    if teamEvents is not None:
        official = teamEvents[teamEvents.Type < 10]
        if len(official) > 0:
            firstEvent = official.iloc[0]['Event']
            playPoints, awardPoints = teamAtEvent(team, firstEvent)
        
    return {'team': team, 'playPoints': playPoints, 'awardPoints': awardPoints}

def main():
    global teams
    pool = Pool()
    teamData = {}
    teamList = gen.readTeamListCsv(currentYear, ['Teams'])['Teams']
    
    for team in teamList:
        teams[team] = {'playValues': [], 'awardValues': [], 'totalValues': []}
        for year in years:
            teams[team][str(year)] = {'playPoints': 0, 'awardPoints': 0}
        
    for idx, year in enumerate(years):
        gen.progressBar(idx, len(years))
        teamData[str(year)] = []
        teamData[str(year)] = pool.map(partial(getData, year), teamList)
    
    for year in teamData:
        for t in teamData[year]:
            teams[t['team']][year]['playPoints'] = t['playPoints']
            teams[t['team']][year]['awardPoints'] = t['awardPoints']
                
    outData = []
    for team in teams:
        playValues = [teams[team][str(year)]['playPoints'] for year in years]
        awardValues = [teams[team][str(year)]['awardPoints'] for year in years]
        totalValues = [teams[team][str(year)]['playPoints'] + teams[team][str(year)]['awardPoints'] for year in years] 
        
        avgPlay = stat.mean(playValues)
        avgAward = stat.mean(awardValues)
        avgTotal = stat.mean(totalValues)
        
        maxPlay = max(playValues)
        maxAward = max(awardValues)
        maxTotal = max(totalValues)
        
        teamObj = {'Team': team[3:],
                   'Average Play': avgPlay,
                   'Average Award': avgAward,
                   'Average Total': avgTotal,
                   'Max Play': maxPlay,
                   'Max Award': maxAward,
                   'Max Total': maxTotal}
                   
        for idx, year in enumerate(years):
            teamObj[str(year) + ' Play'] = playValues[idx]
            teamObj[str(year) + ' Award'] = awardValues[idx]
            teamObj[str(year) + ' Total'] = totalValues[idx]
        
        outData.append(teamObj)
    
    colOrder = ['Team', 'Average Play', 'Average Award', 'Average Total', 'Max Play', 'Max Award', 'Max Total']
    for year in range(currentYear - yearRange + 1, currentYear + 1):
        colOrder.append(str(year) + ' Play')
        colOrder.append(str(year) + ' Award')
        colOrder.append(str(year) + ' Total')
    
    gen.listOfDictToCSV("Worldwide Regional", outData, colOrder)
                
if __name__ == "__main__":
    main()