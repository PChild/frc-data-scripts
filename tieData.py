import tbapy

tba = tbapy.TBA('DJRE7IGB1IBTCtvpZfFnn7aZfBWoY9bTIZfQFY7CVBZ8tWeNRX6x0XdISQ63skHv')

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

f = open("tieData.csv", 'w', encoding='utf-8')

for prop in tieData[0].keys():
    f.write(prop + ", ")
f.write("\n")

for year in tieData:
    for prop in year.keys():
        f.write(str(year[prop]) + ", ")
    f.write("\n")
f.close()