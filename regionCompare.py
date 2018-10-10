import gen
import copy
import json
import geoDicts
import pandas as pd
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from adjustText import adjust_text

YEAR = 2018
tba = gen.setup()

def generateRegionTeamMap(force=False):
    fileName = 'teamRegionMapping.json'
    
    try:
        if not force:
            regionTeams = json.load(open(fileName))
            print('Read region teams from file.')
    except:
        force = True
    if force:
        regionTeams = {}
        usRegions = {'California': ['CA'],
                   'Texas': ['TX', 'NM'],
                   'Midwest': ['OK','ND', 'SD', 'KS', 'WI', 'IL', 'NE', 'MO', 'IA', ],
                   'Desert': ['NV', 'AZ'],
                   'New York': ['NY'],
                   'Bluegrass': ['TN', 'KY'],
                   'Mountain': ['CO', 'UT', 'ID', 'WY', 'MT'],
                   'South': ['AR', 'LA', 'MS', 'AL'],
                   'Florida': ['FL'],
                   'Minnesota': ['MN'],
                   'WOW': ['PA', 'WV', 'OH'],
                   'South Carolina': ['SC'],
                   'Hawaii': ['HI']}           
        caRegions = {'Quebec': ['QC'],
                     'Alberta': ['AB', 'SK'],
                     'Ontario': ['ON'],
                     'British Columbia': ['BC']}
        tmpRegions = copy.deepcopy(usRegions)
        for region in tmpRegions:
                for state in tmpRegions[region]:
                    if region in usRegions:
                        usRegions[region].append(geoDicts.states[state])
        tmpRegions = copy.deepcopy(caRegions)
        for region in tmpRegions:
                for prov in tmpRegions[region]:
                    if region in caRegions:
                        caRegions[region].append(geoDicts.provs[prov])
        usList = []
        for region in usRegions:
            usList += usRegions[region]    
        caList = []
        for region in caRegions:
            caList += caRegions[region]
            
        nonNaRegions = ['Australia', 'Turkey', 'Mexico']
        china = ['China', 'Chinese Taipei', 'Singapore']
        southAmerica = ['Brazil', 'Chile', 'Colombia', 'Paraguay']
        europe = ['United Kingdom', 'France', 'Netherlands', 'Switzerland', 'Croatia', 'Czech Republic', 'Germany', 'Poland', 'Sweden', 'Norway']
        
        for region in usRegions:
            regionTeams[region] = []
        for region in caRegions:
            regionTeams[region] = []
        for region in nonNaRegions:
            regionTeams[region] = []
        regionTeams['Europe'] = []
        regionTeams['China'] = []
        regionTeams['South America'] = []
        
        districts = tba.districts(YEAR)
        districtNames = [item['display_name'].replace('FIRST', '').replace(' In ', '').strip() for item in districts]
        districtKeys = [item['key'] for item in districts]
        distTeams = []
        
        for idx, district in enumerate(districtKeys):
            if district != '2018tx':
                districtTeams = tba.district_teams(district, False, True)
                regionTeams[districtNames[idx]] = districtTeams
                distTeams += districtTeams        
            
        teams = []
        print('Fetching teams')
        for page in tqdm(range(0,20)):
                newTeams = tba.teams(page, YEAR)
                if newTeams == []:
                    break;
                else:
                    teams += newTeams         
        baseTeams = teams[:]
        teamCount = len(baseTeams)
        for team in baseTeams:
            if team['key'] in distTeams:
                teams.remove(team)
        baseTeams = teams[:]      
        notInSetCount = 0
        notRepresented = {}
        print('Problem teams:')
        for team in baseTeams:
            notListed = True
            if team['country'] in nonNaRegions:
                    regionTeams[team['country']].append(team['key'])
                    notListed = False
            if team['country'] in europe:
                    regionTeams['Europe'].append(team['key'])
                    notListed = False
            if team['country'] in china:
                    notListed = False
                    regionTeams['China'].append(team['key'])
            if team['country'] in southAmerica:
                    notListed = False
                    regionTeams['South America'].append(team['key'])
            if team['state_prov'] in usList and team['country'] == 'USA':
                for region in usRegions:
                    if team['state_prov']  in usRegions[region]:
                        regionTeams[region].append(team['key'])
                        notListed = False
                        break
            if team['state_prov'] in caList and team['country'] in ['Canada', 'CA']:
                for region in caRegions:
                    if team['state_prov'] in caRegions[region]:
                        regionTeams[region].append(team['key'])
                        notListed = False
                        break
            if notListed:
                print(team['key'])
                if team['country'] in notRepresented:
                    notRepresented[team['country']] += 1
                else:
                    notRepresented[team['country']] = 1
                    
            notInSetCount += notListed
            teamIdx = next((index for (index, d) in enumerate(teams) if d['key'] == team['key']), None)
            if teamIdx is not None:
                del teams[teamIdx]
        countryList = []
        for country in notRepresented:
            countryList.append((country, notRepresented[country]))
        countryList = sorted(countryList, key= lambda entry: entry[1], reverse=True)
        print(notInSetCount, 'out of', teamCount, 'are not represented.')
        print(len(countryList), 'countries are not represented.')
        for entry in countryList:
            print(entry[0], '-', entry[1], 'teams')
        
        json.dump(regionTeams, open(fileName, 'w'))
        
    return regionTeams    

def isOutlier(value, eloList):
    q1, q3 = np.percentile(eloList, [25, 75])
    iqr = q3 - q1
    
    lowerBound = q1 - (iqr * 1.5)
    upperBound = q3 + (iqr * 1.5)
    
    return value > upperBound or value < lowerBound

def isTop(value, eloList, topRange = 4):
    eloList = sorted(eloList, reverse=True)
    
    return value in eloList[:topRange]

def generateChart(regionTeams, outliersMarked = 5):
    eloData = pd.read_csv('2018_Elo_end.csv')
    
    regionElos = {}
    
    for region in regionTeams:
        regionElos[region] = []
        for team in regionTeams[region]:
            teamData = eloData[eloData.Team == int(team[3:])]
            if not teamData.empty:
                teamElo = teamData['Elo'].values[0]
                regionElos[region].append(teamElo)
                
    eloFrame = pd.DataFrame.from_dict(regionElos, orient='index').transpose()
    
    medData = []
    for region in eloFrame.columns:
        medData.append((region, eloFrame[region].median()))
    
    medData = sorted(medData, key= lambda entry: entry[1], reverse=True)
    colOrder = [entry[0] for entry in medData]
    
    maxTeams = max([len(regionTeams[region]) for region in colOrder])
    widths = [len(regionTeams[region])/maxTeams + .1 for region in colOrder]
    
    
    eloFrame = eloFrame[colOrder]
    
    ax = eloFrame.plot(kind='box', title='FRC 2018 Elo Ratings by Region', figsize=(30,15), rot=-90, widths=widths, showmeans=True, meanline=True)
    ax.set_xlabel('Region')
    ax.set_ylabel('Elo Rating')
    ax.yaxis.grid(linestyle='--')
    
    textData = []
    for region in regionTeams:
        for team in regionTeams[region]:
            teamData = eloData[eloData.Team == int(team[3:])]
            if not teamData.empty:
                teamElo = teamData['Elo'].values[0]
                if isOutlier(teamElo, regionElos[region]) and isTop(teamElo, regionElos[region], outliersMarked):
                    textData.append((colOrder.index(region) + 1, teamElo, team[3:]))
    texts = [ax.text(entry[0], entry[1], entry[2], ha='center', va='center') for entry in textData]
    adjust_text(texts)
    
    plt.savefig('FRC 2018 Elo Ratings by Region')
    
    return ax

def main():
    regionTeams = generateRegionTeamMap()
    generateChart(regionTeams, 6)
    
    
if __name__ == '__main__':
    main()