import tbapy
tba = tbapy.TBA('DJRE7IGB1IBTCtvpZfFnn7aZfBWoY9bTIZfQFY7CVBZ8tWeNRX6x0XdISQ63skHv')

years = [2016, 2017, 2018]

cmpData = {'2016': {'cmpmo': {'slots': 600, 'districts': {'chs': 25, 'in': 9, 'fim': 76, 'mar': 22, 'nc': 10, 'ne': 34, 'pnw': 30, 'pch': 12}}},
           '2017': {'north': {'slots': 402, 'districts': {'chs': 23,'fim': 82,'in': 10,'mar': 22,'ne': 37,'ont': 29}},
                    'south': {'slots': 402, 'districts': {'isr': 16, 'nc': 15, 'pnw': 39, 'pch': 18}}},
           '2018': {'north': {'slots': 402, 'districts': {'chs': 21,'fim': 89,'in': 9,'mar': 22,'ne': 37,'ont': 29}},
                    'south': {'slots': 402, 'districts': {'isr': 15, 'nc': 14, 'pnw': 32, 'pch': 16}}}}
           
properties = ['slots', 'distSlots', 'regSlots', 'teams', 'distTeams', 'regTeams', 'waitList']

data = {}

f = open("champs_stats.csv", 'w')

for year in years:
    yearData = {}    
    distData = {}
    y = str(year)

    for p in properties:
        yearData[p] = 0
        
    print("Fetching events for " + y)
    events = tba.events(year)
    
    print("Fetching district lists for " + y)
    districts = tba.districts(year)

    totalFRCTeams = 0
    regionalCount = 0
    
    for page in range(0,20):
        print("Fetching page " + str(page) + " of teams for " + y)
        pageData = len(tba.teams(page, year, True, True))
        totalFRCTeams += pageData
        if pageData is 0:
            break
        
    for district in districts:
        dist = district['key']
        abbv = district['abbreviation']
        print("Fetching district teams for " + str(dist))
        distSize = len(tba.district_teams(dist))
        distData[abbv] = distSize
    
    for event in events:
        regional = event['event_type'] == 0
        
        if regional:
            regionalCount += 1

    yearData['regionals'] = regionalCount
    
    for p in properties:
        f.write(p + ", ")
    f.write("\n")
    
    for comp in cmpData[y]:
        yearData[comp] = {}
        cmp = cmpData[y][comp]
    
        distTeams = 0
        for dist in cmp['districts']:
            distTeams += distData[dist]
        
        compInfo = yearData[comp]
        slots = cmp['slots']
        distSlots = sum(cmp['districts'].values())
        cmpEvents = len(cmpData[y])
        
        regSlots = round(regionalCount / cmpEvents  * 7)
        waitList = slots - distSlots - regSlots
        regTeams = round(totalFRCTeams / cmpEvents - distTeams)
        teams = round(totalFRCTeams / cmpEvents)
        
        for p in properties:
            compInfo[p] = eval(p)
            yearData[p] += eval(p)  
    data[y] = yearData   
        
for year in years:
    y = str(year)
    d = data[y]
    
    f.write("Year" + ", " + "Regionals" + ", ")
    for p in properties:
        f.write(p + ", ")
    f.write('\n')
    
    f.write(y + ", " + str(d['regionals'])  + ", ")
    for p in properties:
        f.write(str(d[p]) + ", ")
    f.write('\n')
    
    for e in d:
        if e not in properties and e is not 'regionals':
            cI = d[e]
            f.write(" , , ")
            for p in properties:
                f.write(str(cI[p]) + ", ")
            f.write('\n')
    f.write('\n')
f.close()