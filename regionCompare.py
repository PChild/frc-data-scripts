import gen
import copy
import json
import geoDicts
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt

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
                   'Mountain': ['CO', 'UT', 'ID', 'WY', 'MT'],
                   'South': ['AR', 'LA', 'MS', 'AL'],
                   'Florida': ['FL'],
                   'Minnesota': ['MN'],
                   'WOW': ['PA', 'WV', 'OH'],
                   'South Carolina': ['SC'],
                   'Hawaii': ['HI']}           
        caRegions = {'Quebec': ['QC'],
                     'Alberta': ['AB'],
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
        nonNaRegions = ['Australia', 'Turkey', 'Mexico', 'Brazil', 'China']
        districts = [item.key for item in tba.districts(YEAR)]
        distTeams = []
        for district in districts:
            if district != '2018tx':
                districtTeams = tba.district_teams(district, False, True)
                regionTeams[district[4:].upper()] = districtTeams
                distTeams += districtTeams        
        for region in usRegions:
            regionTeams[region] = []
        for region in caRegions:
            regionTeams[region] = []
        for region in nonNaRegions:
            regionTeams[region] = []    
        teams = []
        print('Fetching teams')
        for page in tqdm(range(0,20)):
                newTeams = tba.teams(page, YEAR)
                if newTeams == []:
                    break;
                else:
                    teams += newTeams         
        baseTeams = teams[:]
        print('Removing district teams')
        for team in tqdm(baseTeams):
            if team['key'] in distTeams:
                teams.remove(team)
        baseTeams = teams[:]      
        print('\nFinding non NA teams')
        notInSetCount = 0
        for team in tqdm(baseTeams):
            notListed = True
            if team['country'] in nonNaRegions:
                    regionTeams[team['country']].append(team['key'])
                    notListed = False
            else:
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
            notInSetCount += notListed
            teamIdx = next((index for (index, d) in enumerate(teams) if d['key'] == team['key']), None)
            if teamIdx is not None:
                del teams[teamIdx]
        print('\n',notInSetCount, 'out of', len(baseTeams), 'are not represented in regions.')
        json.dump(regionTeams, open(fileName, 'w'))
    return regionTeams    


def main():
    regionTeams = generateRegionTeamMap()
    eloData = pd.read_csv('2018_Elo_End.csv')
    
    regionElos = {}
    
    for region in regionTeams:
        regionElos[region] = []
        for team in regionTeams[region]:
            teamData = eloData[eloData.Team == int(team[3:])]
            if not teamData.empty:
                teamElo = teamData['Elo'].values[0]
                regionElos[region].append(teamElo)
                
    
    eloFrame = pd.DataFrame.from_dict(regionElos, orient='index').transpose()
    
    meanData = []
    for region in eloFrame.columns:
        meanData.append((region, eloFrame[region].median()))
    
    meanData = sorted(meanData, key= lambda entry: entry[1], reverse=True)
    colOrder = [entry[0] for entry in meanData]
    
    eloFrame = eloFrame[colOrder]
    
    ax = eloFrame.plot(kind='box', title='FRC 2018 Elo Ratings by Region', figsize=(30,15), rot=-90)
    ax.set_xlabel('Region')
    ax.set_ylabel('Elo Rating')
    ax.yaxis.grid(linestyle='--')
    
    plt.savefig('FRC 2018 Elo Ratings by Region')
    
    
if __name__ == '__main__':
    main()