import gen

tba = gen.setup()

YEAR = 2018

#Excluding MAR for now, I don't know how to handle partial inclusing of PA
DISTRICTS = ['chs', 'fim', 'in', 'isr', 'ne', 'nc', 'ont', 'pch', 'pnw']

DISTRICT_STATES = {'chs': ['Virginia', 'Maryland', 'District of Columbia', 'DC', 'VA, ''MD'],
                   'fim': ['Michigan', 'MI'],
                    'in': ['Indiana', 'IN'],
                    'isr': ['Israel'],
                    'ne': ['Massachusetts', 'Maine', 'Rhode Island', 'New Hampshire', 'Connecticut', 'Vermont', 'MA', 'ME', 'RI', 'NH', 'CT', 'VT'],
                    'nc': ['North Carolina', 'NC'],
                    'ont': ['Ontario', 'ONT'],
                    'pch': ['Georgia', 'GA'],
                    'pnw': ['Washington', 'Oregon', 'WA', 'OR']}


districtStats = {}


for district in DISTRICTS:
    districtStats[district] = {}

yearRange = range(1992, YEAR + 1)

for count, year in enumerate(yearRange):
    gen.progressBar(count, len(yearRange))
    
    currentDistricts = tba.districts(year)

    for district in DISTRICTS:
        districtStats[district][str(year)] = {}
        districtStats[district][str(year)]['dist'] = False
        districtStats[district][str(year)]['teams'] = 0
    
    for district in currentDistricts:
        if district['abbreviation'] not in ['mar', 'tx']:
            districtStats[district['abbreviation']][str(year)]['dist'] = True
    
    
    teams = []
    for page in range(0,20):
        try:
            newTeams = tba.teams(page, year, True)
            
            if newTeams == []:
                break;
            else:
                teams += newTeams
        except:
            pass
    for team in teams:
        if team['country'] in DISTRICT_STATES['isr']:
            districtStats['isr'][str(year)]['teams'] += 1
        
        for district in DISTRICTS:
            if team['state_prov'] in DISTRICT_STATES[district]:
                districtStats[district][str(year)]['teams'] += 1

districtTable = []
for d in districtStats:
    dist = districtStats[d]

    for year in dist:
        isDist = districtStats[d][year]['dist']
        teams = districtStats[d][year]['teams']
        districtTable.append({'dist': d, 'year': year, 'isDist': isDist, 'teams': teams})

gen.listOfDictToCSV('districtGrowth', districtTable)