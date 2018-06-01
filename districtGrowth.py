import gen
import geocoder

tba = gen.setup()

YEAR = 2018

DISTRICTS = ['chs', 'fim', 'in', 'isr', 'mar', 'ne', 'nc', 'ont', 'pch', 'pnw']

DISTRICT_STATES = {'chs': ['Virginia', 'Maryland', 'District of Columbia', 'DC', 'VA, ''MD'],
                   'fim': ['Michigan', 'MI'],
                    'in': ['Indiana', 'IN'],
                    'isr': ['Israel'],
                    'mar': ['New Jersey', 'Pennsylvania', 'Delaware', 'NJ', 'PA', 'DE'],
                    'ne': ['Massachusetts', 'Maine', 'Rhode Island', 'New Hampshire', 'Connecticut', 'Vermont', 'MA', 'ME', 'RI', 'NH', 'CT', 'VT'],
                    'nc': ['North Carolina', 'NC'],
                    'ont': ['Ontario', 'ON'],
                    'pch': ['Georgia', 'GA'],
                    'pnw': ['Washington', 'Oregon', 'WA', 'OR']}


districtStats = {}

inMar = []
outOfMar = []
problemTeams = []
def handlePA(team, year):
    # Mid Atlantic Robotics Bylaws Article 1 Section 2 define the PA part of MAR as 'the counties of Pennsylvania including Harrisburg, eastward'
    # Harrisburg's longitude is listed as -76.884 , I used -77 as it's a round number and gives a ~7 mile margin.
    HARRISBURG_WEST_LON = -77
    
    if team['team_number'] in inMar:
        addToDistrict(team, 'mar', year)
    elif team['team_number'] in outOfMar:
        pass
    else:
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
                inMar.append(team['team_number'])
                addToDistrict(team, 'mar', year)
        else:
            outOfMar.append(team['team_number'])    

def addToDistrict(team, district, year):
    districtStats[district]['years'][year]['teams'] += 1
    districtStats[district]['currentTeams'].append(team['team_number'])


yearRange = range(1992, YEAR + 1)

for district in DISTRICTS:
    districtStats[district] = {'currentTeams': [], 'prevTeams': [], 'years': {}}
    
    for year in yearRange:
        districtStats[district]['years'][str(year)] = {'dist': False, 'teams': 0, 'added': 0, 'lost': 0}


for count, y in enumerate(yearRange):
    gen.progressBar(count, len(yearRange))
    
    currentDistricts = tba.districts(y)
    year = str(y)
    
    for district in currentDistricts:
        if district['abbreviation'] != 'tx':
            districtStats[district['abbreviation']]['years'][year]['dist'] = True
    
    teams = []
    for page in range(0,20):
        try:
            newTeams = tba.teams(page, y)
            
            if newTeams == []:
                break;
            else:
                teams += newTeams
        except:
            pass
        
    for team in teams:
        if team['country'] in DISTRICT_STATES['isr']:
            addToDistrict(team, 'isr', year)
        for district in DISTRICTS:
            if team['state_prov'] in DISTRICT_STATES[district]:
                if team['state_prov'] in ['Pennsylvania', 'PA']:
                    handlePA(team, year)
                else:
                    addToDistrict(team, district, year)
                    
    for district in DISTRICTS:
        d = districtStats[district]
        for team in d['currentTeams']:
            if team not in d['prevTeams']:
                d['years'][year]['added'] += 1
        for team in d['prevTeams']:
            if team not in d['currentTeams']:
                d['years'][year]['lost'] += 1
        d['prevTeams'] = d['currentTeams']
        d['currentTeams'] = []

#MAR validation checking
marTeams = tba.district_teams('2018mar')
for team in marTeams:
    if team['team_number'] in outOfMar:
        print(team['team_number'], "is actually in MAR")


#Prep table and then save it out
districtTable = []
for d in districtStats:
    dist = districtStats[d]['years']

    for year in dist:
        isDist = dist[year]['dist']
        teams = dist[year]['teams']
        added = dist[year]['added']
        lost = dist[year]['lost']
        districtTable.append({'dist': d, 'year': year, 'isDist': isDist, 'teams': teams, 'added': added, 'lost': lost})

gen.listOfDictToCSV('districtGrowth', districtTable)