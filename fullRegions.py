import gen
import copy
import json
import geoDicts
import geocoder
from tqdm import tqdm

fileName = 'allTimeTeamRegionMapping.json'

usRegions = {'California': ['CA'],
            'Chesapeake' : ['VA', 'MD', 'DC'],
            'Midwest': ['OK','ND', 'SD', 'KS', 'WI', 'IL', 'NE', 'MO', 'IA', ],
            'Desert': ['NV', 'AZ'],
            'New York': ['NY'],
            'Bluegrass': ['TN', 'KY'],
            'Mountain': ['CO', 'UT', 'ID', 'WY', 'MT'],
            'South': ['AR', 'LA', 'MS', 'AL'],
            'Florida': ['FL'],
            'Minnesota': ['MN'],
            'WOW': ['WV', 'OH'],
            'South Carolina': ['SC'],
            'Peachtree': ['GA'],
            'Michigan': ['MI'],
            'Hawaii': ['HI'],
            'Texas': ['TX', 'NM'],
            'Indiana': ['IN'],
            'Mid-Atlantic': ['NJ', 'DE'],
            'New England': ['MA', 'ME', 'RI', 'NH', 'CT', 'VT'],
            'North Carolina': ['NC'],
            'Pacific Northwest': ['WA', 'OR', 'AK']}     
    
caRegions = {'Quebec': ['QC', 'NS', 'NB'],
             'Alberta': ['AB', 'SK'],
             'Ontario': ['ON'],
             'British Columbia': ['BC'],}

problemTeams =[]
def handlePA(team):
    key = team['key']
    # Mid Atlantic Robotics Bylaws Article 1 Section 2 define the PA part of MAR as 'the counties of Pennsylvania including Harrisburg, eastward'
    # Harrisburg's longitude is listed as -76.884 , I used -77 as it's a round number and gives a ~7 mile margin.
    HARRISBURG_WEST_LON = -77
    try:
        if team['postal_code']:
            teamLng  = geocoder.osm(team['postal_code']).lng
        else:
            teamLng = geocoder.osm(team['city'] + ", " + team['state_prov']).lng
    except Exception as e:
        print(e)
        teamLng = -90
        problemTeams.append(team['team_number'])

    if teamLng:
        if teamLng > HARRISBURG_WEST_LON:
            regionTeams['Mid-Atlantic'].append(key)
        else:
            regionTeams['WOW'].append(key)

regionTeams = {}
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
    
nonNaRegions = ['Australia', 'Turkey', 'Mexico', 'Israel', 'Africa', 'Oceania']
china = ['China', 'Chinese Taipei', 'Singapore']
southAmerica = ['Brazil', 'Chile', 'Colombia', 'Paraguay', 'Ecuador']
africa = ['Ethiopia', 'South Africa', 'Libya']
europe = ['United Kingdom', 'Kingdom', 'Armenia', 'Italy', 'Bosnia-Herzegovina', 'Spain', 'Denmark', 'Greece', 'France', 'Netherlands', 'Switzerland', 'Croatia', 'Czech Republic', 'Germany', 'Poland', 'Sweden', 'Norway']
oceania = ['Vietnam', 'New Zealand', 'Japan', 'Indonesia']

for region in usRegions:
    regionTeams[region] = []
for region in caRegions:
    regionTeams[region] = []
for region in nonNaRegions:
    regionTeams[region] = []
regionTeams['Europe'] = []
regionTeams['China'] = []
regionTeams['South America'] = [] 
    
tba = gen.setup()
teams = []
print('Fetching teams')
for page in tqdm(range(0,40)):
        newTeams = tba.teams(page)
        if newTeams == []:
            break;
        else:
            teams += newTeams         
     
notInSetCount = 0
notRepresented = {}
print('Problem teams:')
for team in teams:
    notListed = True
    country = team['country']
    region = team['state_prov']
    key = team['key']
    
    if country in nonNaRegions:
            regionTeams[country].append(key)
            notListed = False
    if country in europe:
            regionTeams['Europe'].append(key)
            notListed = False
    if country in china:
            notListed = False
            regionTeams['China'].append(key)
    if country in southAmerica:
            notListed = False
            regionTeams['South America'].append(key)
    if country in africa:
            notListed = False
            regionTeams['Africa'].append(key)
    if country in oceania:
            notListed = False
            regionTeams['Oceania'].append(key)
    if country in ['USA', 'US']:
        if region in  ['PA', 'Pennsylvania']:
            notListed = False
            handlePA(team)
        else:
            for area in usRegions:
                if region in usRegions[area]:
                    regionTeams[area].append(key)
                    notListed = False
                    break
    if region in caList and country in ['Canada', 'CA']:
        for area in caRegions:
            if region in caRegions[area]:
                regionTeams[area].append(key)
                notListed = False
                break
    if notListed:
        print(key)
        if country in notRepresented:
            notRepresented[country] += 1
        else:
            notRepresented[country] = 1
            
    notInSetCount += notListed
countryList = []
for country in notRepresented:
    countryList.append((country, notRepresented[country]))
countryList = sorted(countryList, key= lambda entry: entry[1], reverse=True)
print(notInSetCount, 'out of', len(teams), 'are not represented.')
print(len(countryList), 'countries are not represented.')
for entry in countryList:
    print(entry[0], '-', entry[1], 'teams')

json.dump(regionTeams, open(fileName, 'w'))