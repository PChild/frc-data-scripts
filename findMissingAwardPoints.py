import gen
import eventTypes

tba = gen.setup()

year = 2019
currentWeek = 6

for event in tba.events(year):
    if event['event_type'] == eventTypes.DISTRICT:
        if event['week'] + 1 < currentWeek:
            awardsTotal = 0
            
            distPoints = tba.event_district_points(event['key'])['points']
            for team in distPoints:
                awardsTotal += distPoints[team]['award_points']
            
            if awardsTotal < 60:
                print(event['key'], 'is missing award points')