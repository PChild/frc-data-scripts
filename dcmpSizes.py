import gen

tba = gen.setup()

YEAR = 2018
DISTRICTS = ['chs', 'fim', 'in', 'isr', 'mar', 'ne', 'nc', 'ont', 'pch', 'pnw']
DCMP_EVENTS = [2, 5]

dcmpData = {}

for district in DISTRICTS:
    dcmpData[district] = {}

for y in range(2009, YEAR + 1):
    for district in DISTRICTS:
        try:
            districtEvents = tba.district_events(str(y) + district, True, False)
            
            #Avoid double counting events with divisions      
            validTypes = DCMP_EVENTS[:]
            hasDivisions = False
            dcmpSize = 0
            
            for event in districtEvents:
                hasDivisions = hasDivisions or event['event_type'] == 5
                if hasDivisions:
                    validTypes.remove(2)
                    break
                
            for event in districtEvents:
                if event['event_type'] in validTypes:
                    dcmpSize += len(tba.event_teams(event['key'], False, True))
            dcmpData[district][str(y)] = dcmpSize
            print(district, y , "dcmp size:", dcmpSize)
        except:
            pass

gen.writeJsonFile('dcmpSizes', dcmpData)