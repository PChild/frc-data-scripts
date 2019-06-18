import eventTypes
import gen

tba = gen.setup()

eventData = []

for event in tba.events(2019):
    if event['event_type'] == eventTypes.REGIONAL:
        eventData.append({'Event': event['key'], 'Teams': len(tba.event_teams(event['key'], False, True))})
    
gen.listOfDictToCSV('2019 Event Sizes', eventData, ['Event', 'Teams'])