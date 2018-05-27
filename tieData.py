import gen

tba = gen.setup()

tieData = []

YEARS = [2010, 2011, 2012, 2013, 2014, 2016, 2017, 2018]

for year in YEARS:
    print("Processing " + str(year))
    
    matchCount = 0
    tieCount = 0
    
    for event in tba.events(year, True, False):
        if event['event_type'] in range(0,10):
            print("Fetching matches for " + event['key'])
            for match in tba.event_matches(event['key'], True):
                tieCount += match['winning_alliance'] not in ['red', 'blue']
                matchCount += 1
    tieData.append({'year': year, 'matches': matchCount, 'ties': tieCount})

gen.listOfDictToCSV("tieData", tieData)