import gen
import copy
import geoDicts
from tqdm import tqdm

YEAR = 2018
tba = gen.setup()

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

naRegions = {**usRegions, **caRegions}
tmpRegions = copy.deepcopy(naRegions)
for region in tmpRegions:
        for state in tmpRegions[region]:
            if region in usRegions:
                naRegions[region].append(geoDicts.states[state])
            else:
                naRegions[region].append(geoDicts.provs[state])
            
nonNaRegions = ['Australia', 'Turkey', 'Mexico', 'Brazil', 'China']

districts = [item.key for item in tba.districts(YEAR)]
distTeams = []
for district in districts:
    if district != '2018tx':
        districtTeams = tba.district_teams(district, False, True)
        regionTeams[district[4:]] = districtTeams
        distTeams += districtTeams
        
for region in naRegions:
    regionTeams[region] = []

for region in nonNaRegions:
    regionTeams[region] = []
    
teams = []
for page in range(0,20):
        newTeams = tba.teams(page, YEAR)
        if newTeams == []:
            break;
        else:
            teams += newTeams
            
baseTeams = teams[:]
for team in baseTeams:
    if team['key'] in distTeams:
        teams.remove(team)
        
for team in teams:
    for region in usRegions:
        if team['state_prov'] in naRegions[region]:
            regionTeams[region].append(team['key'])
            teams.remove(team)
        if team['country'] in nonNaRegions:
            regionTeams[team['country']].append(team['key'])
            teams.remove(team)
    