import gen
import geoDicts

WOW = ['OH', 'WV']
CHS = ['VA', 'MD', 'DC']
NE = ['RI', 'MA', 'ME', 'VT', 'NH', 'CT']
MAR = ['DE', 'NJ']
other = ['ON', 'NY', 'PA']

regions = [WOW, CHS, NE, MAR, other]

areas = WOW + CHS + NE + MAR + other

tba = gen.setup()

def inMAR(event):
    # Mid Atlantic Robotics Bylaws Article 1 Section 2 define the PA part of MAR as 'the counties of Pennsylvania including Harrisburg, eastward'
    # Harrisburg's longitude is listed as -76.884 , I used -77 as it's a round number and gives a ~7 mile margin.
    HARRISBURG_WEST_LON = -77
    
    return event['lng'] > HARRISBURG_WEST_LON

data = []
years = range(2011, 2019)
for idx, year in enumerate(years):
    gen.progressBar(idx, len(years))
    yearData = {'WOW': 0, 'CHS': 0, 'NE': 0, 'MAR': 0, 'ON': 0, 'NY': 0}
    yearEvents = tba.events(year)
    
    for event in yearEvents:
        if event['event_type'] == 0:
            if event['state_prov'] in areas:
                yearData['WOW'] += int(event['state_prov'] in WOW)
                yearData['CHS'] += int(event['state_prov'] in CHS)
                yearData['NE'] += int(event['state_prov'] in NE)
                yearData['MAR'] += int(event['state_prov'] in MAR)
                yearData['ON'] += int(event['state_prov'] == 'ON')
                yearData['NY'] += int(event['state_prov'] == 'NY')
                
                if event['state_prov'] == 'PA':
                    yearData['MAR'] += int(inMAR(event))
                    yearData['WOW'] += int(not inMAR(event))
    data.append(yearData)
    
gen.listOfDictToCSV("neRegionals", data)            