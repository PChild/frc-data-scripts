import gen
import math
import statistics as stat
from tqdm import tqdm
from scipy.special import erfinv

tba = gen.setup()
NORMAL_EVENTS = [0,1]

def buildTeamList(year=2019, pages=18):
    teamList = []
    for page in tqdm(range(0, pages)):
        teamList += tba.teams(page, year, False, True)
    
    return teamList

def getPlayPoints(team, event):
    draftPoints = 0
    rankPoints = 0
    elimPoints = 0
    teamRank = 0
    
    teamMatches = gen.teamEventMatches(team, event)
    tmpRk = []
    
    try:
        rK = gen.readEventCsv(event, 'rankings')
        
        if str(rK['Team'][0]).isnumeric():
            rK['Team'] = 'frc' + rK['Team'].astype(str)
        tmpRk = rK[rK.Team == team]
    
        if len(tmpRk) > 0:
            teamRank = rK[rK.Team == team]['Rank'].iloc[0]
            teamCount = len(rK)
            
            alpha = 1.07
            rankPoints = math.ceil(abs(erfinv( (teamCount - 2 * teamRank + 2) /  (alpha * teamCount)) * 10 / erfinv( 1 / alpha ) + 12 ))
        
            names = ['captain', 'firstPick', 'secondPick']
    
            aL = gen.readEventCsv(event, 'alliances', names)
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
                    draftPoints = 17 - int(alliance['number'])
                elif alliance['pick'] == 2:
                    draftPoints = int(alliance['number'])
        
            if teamMatches is not None:
                for idx, match in teamMatches.iterrows():
                    if match['key'].split('_')[1][:2] != 'qm':
                        if gen.matchResult(team, match, False) == 'WIN':
                            elimPoints += 5
    except:
        pass
    return [draftPoints, rankPoints, elimPoints, teamRank]

def getAwardPoints(team, event):
    ROBOT_AWARDS = [16, 17, 20, 21, 29, 71]
    OTHER_AWARDS = [11, 13, 18, 22, 27, 30]
    NO_POINTS = [1, 2, 5, 14]
    CA = 0
    EI = 9
    WF = 3
    DEANS = 4
    RAS = 10
    RI = 15
    WILDCARD = 68
    
    numberToName = {0: 'CA', 1: 'Winner', 2: 'Finalist', 9: 'EI', 3: 'WF', 4: 'DEANS', 10: 'RAS', 15: 'RI', 16: 'ID', 17: 'Quality', 20: 'Creativity', 21: 'EE', 29: 'Control', 71: 'Auto',
                    11: 'GP', 13: 'Judges', 18: 'Safety', 22: 'Ent', 27: 'Imagery', 30: 'Spirit'}
    awardValues = {CA: 60, EI: 45, RAS: 25, RI: 15, WF: 10, DEANS: 5, WILDCARD: 0, 'ROBOT': 20, 'OTHER': 5, 'NONE': 0}
    
    awardPoints = 0
    awardNames = []

    tya = gen.readTeamCsv(team, 'awards', event[:4], ['Event', 'Type', 'Name'])
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
                
            if row['Type'] in numberToName.keys():
                awardNames.append(numberToName[row['Type']])
            awardPoints += awardValues[awardType]
    return [awardPoints, ' / '.join(awardNames)]

def fetchNormalEventData(year=2019):
    eventData = {}
    for event in tba.events(year):
        if event['event_type'] in NORMAL_EVENTS:
            eventData[event['key']]= event['week']
    return eventData

def getPerformanceData(team, year):
    team = gen.teamString(team)
    oprs = []
    wins = 0
    losses = 0
    ties = 0
    
    try:
        matches = gen.readTeamCsv(team, 'matches', year)  
        if len(matches) > 0:
            for idx, match in matches.iterrows():
                result = gen.matchResult(team, match)
                wins += 'WIN' == result
                losses += 'LOSS' == result
                ties += 'TIE' == result
    except:
        pass
        
    try:
        events = gen.readTeamCsv(team, 'events', year)
        if len(events) > 0:    
            for idx, e in events.iterrows():                    
                    try:
                        eOprs = gen.readEventCsv(e['Event'], 'opr')
                        teamOPR = eOprs[eOprs.Team == team]['OPR'].values[0]
                        oprs.append(teamOPR)
                    except Exception as e:
                        pass
    except:
        pass
        
        
    if len(oprs) is 0:
        maxOPR = 0
        avgOPR = 0
    else:
        maxOPR = max(oprs)
        avgOPR = stat.mean(oprs)
    
    played = wins + losses + ties
    winPercent = 0
    
    if played > 0:
        winPercent = wins / played
    
    teamKey = gen.teamNumber(team)
    
    return {'Team': teamKey, 
            'Max OPR': maxOPR, 
            'Avg OPR': avgOPR, 
            'Wins': wins, 
            'Losses': losses, 
            'Ties': ties, 
            'Win %': winPercent}