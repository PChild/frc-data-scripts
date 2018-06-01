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
    districtStats[district][year]['teams'] += 1
    districtStats[district][year]['currentTeams'].append(team['team_number'])


for district in DISTRICTS:
    districtStats[district] = {}

yearRange = range(1992, YEAR + 1)

for count, y in enumerate(yearRange):
    gen.progressBar(count, len(yearRange))
    
    currentDistricts = tba.districts(y)
    
    year = str(y)

    for district in DISTRICTS:
        districtStats[district][year] = {}
        districtStats[district][year]['dist'] = False
        districtStats[district][year]['teams'] = 0
        districtStats[district][year]['currentTeams'] = []
    
    for district in currentDistricts:
        if district['abbreviation'] != 'tx':
            districtStats[district['abbreviation']][year]['dist'] = True
    
    
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


marTeams = tba.district_teams('2018mar')
for team in marTeams:
    if team['team_number'] in outOfMar:
        print(team['team_number'], "is actually in MAR")

districtTable = []
for d in districtStats:
    dist = districtStats[d]

    for year in dist:
        isDist = districtStats[d][year]['dist']
        teams = districtStats[d][year]['teams']
        districtTable.append({'dist': d, 'year': year, 'isDist': isDist, 'teams': teams})

gen.listOfDictToCSV('districtGrowth', districtTable)