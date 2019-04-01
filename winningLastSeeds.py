import gen
import eventTypes

tba = gen.setup()

for event in tba.events(2018):
    if event['event_type'] in range(eventTypes.REGIONAL, eventTypes.FOC):
        for idx, alliance in enumerate(tba.event_alliances(event['key'])):
            if idx == 7:
                if alliance['status']['status'] == 'won':
                    print(event['key'], alliance['picks'])