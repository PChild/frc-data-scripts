import gen
import math
import numpy
import random
import pandas as pd
import statistics as stat

def chunk(l, n):
    '''
    Splits a list l into a list of n new lists
    '''
    return [list (i) for i in numpy.array_split(numpy.array(l),n)]

def snr(inList):
    '''
    Signal-to-Noise Ratio of a list of ints
    '''
    return 10 * math.log(stat.mean(inList) ** 2 / stat.stdev(inList) ** 2)

def distributeTeams(quartiles):
    '''
    Takes a list of four quartiles to be distributed into divisions
    Returns list of two acceptable divisions
    '''
    allowedAvgStrDiff = 1.0
    allowedStrDistDiff = 1.0
    allowedTopStrDistDiff = 1.5
    
    divA = []
    divB = []
    
    for teamSet in quartiles:      
        random.shuffle(teamSet)
        splitSize = int(len(teamSet) / 2)
        
        divA += teamSet[:splitSize]
        divB += teamSet[splitSize:]
        
    aPts = sorted([team['points'] for team in divA], reverse=True)
    bPts = sorted([team['points'] for team in divB], reverse=True)
    
    meanA = stat.mean(aPts)
    meanB = stat.mean(bPts)
    
    passesMeanCheck = abs(meanA - meanB) <= allowedAvgStrDiff
        
    passesStrCheck = abs(snr(aPts) - snr(bPts)) <= allowedStrDistDiff
    
    topA = chunk(aPts, 4)[0]
    topB = chunk(bPts, 4)[0]
    
    passesTopStrCheck = abs(snr(topA) - snr(topB)) <= allowedTopStrDistDiff
    
    if passesMeanCheck and passesStrCheck and passesTopStrCheck:
        return [sorted(divA, key= lambda k: int(k['team'][3:])), sorted(divB, key= lambda k: int(k['team'][3:]))]
    else:
        return distributeTeams(quartiles)

if __name__ == "__main__":
    tba = gen.setup()
    
    week6Elo = pd.read_excel('week6elo.xlsx')
    endElo = pd.read_excel('week9elo.xlsx')

    year = 2019
    dist = 'chs'
    dcmp = '2019chcmp'

    distRanks = tba.district_rankings(str(year) + dist)
    
    preDCMPstandings = []
    for team in distRanks:
        preDCMP = 0
        for event in team['event_points']:
            if event['event_key'] != dcmp:
                preDCMP += event['total']
        preDCMPstandings.append({'team': team['team_key'], 'points': preDCMP})
        
    '''
    Sort the pre-DCMP rankings, choose 80 top to send to DMCP, split into quartiles, find acceptable divisions
    '''
    preDCMPstandings = sorted(preDCMPstandings, key= lambda k: k['points'], reverse=True)
    
    preDCMP = [{'Team': int(item['team'][3:]), 'Points': item['points']} for item in preDCMPstandings]
    gen.listOfDictToCSV(str(year) + dist + ' Pre-DCMP Standings', preDCMP, ['Team', 'Points'])
    
#    top80 = preDCMPstandings[0:80]
#    quartiles = chunk(top80, 4)
#    divA, divB = distributeTeams(quartiles)
#    
#    divs = []
#    for idx, i in enumerate(divA):
#        divs.append({'A': i['team'][3:], 'B': divB[idx]['team'][3:]})
#        
#    gen.listOfDictToCSV(dcmp + ' Simulated Divisions', divs, ['A', 'B'])