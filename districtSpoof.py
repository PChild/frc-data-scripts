import gen

tba = gen.setup()

def getSpoofedDistrictData(district, year, spoofDate):
    #Fetch data on district events and current district points
    distString = str(year) + district
    districtEvents = tba.district_events(distString, True)
    districtPoints = tba.district_rankings(distString)
    
    completeEvents = []
    fakeData = []

    #Make a deep copy of district points, remove event data and point total.
    for team in districtPoints:
        fakeData.append(dict(team))
        fakeData[-1]['event_points'] = []
        fakeData[-1]['point_total'] = 0

    #Find district events that were complete by the specified date
    for event in districtEvents:
        if event['end_date'] < spoofDate:
            completeEvents.append(event['key'])
    
    #Only add event data for complete events, increase point totals for valid events
    for teamIdx, team in enumerate(districtPoints):
        for event in team['event_points']:
            if event['event_key'] in completeEvents:
                fakeData[teamIdx]['event_points'].append(event)
                fakeData[teamIdx]['point_total'] += event['total']

    #Sort the list by total points in descending order.
    fakeData = sorted(fakeData, key = lambda k: k['point_total'], reverse=True)    
    
    #Iterate through the faked data and set the ranks values.
    for teamIdx, team in enumerate(fakeData):
        team['rank'] = teamIdx + 1
        
    return processDistrictData(fakeData)

def getDistrictData(district, year):
    distString = str(year) + district
    districtPoints = tba.district_rankings(distString)
    
    return processDistrictData(districtPoints)
    

def handleEvents(data):
    events = []
    
    for event in data:
        events.append(event['total'])
    
    return events
        
def processDistrictData(district):
    distData = []
    for team in district:
        distData.append({'rank': team['rank'], 'total': team['point_total'], 'team': team['team_key'], 'events': handleEvents(team['event_points'])})
    
    return distData
    
dataTest = getSpoofedDistrictData('chs', 2018, '2018-03-17')