import gen
#import pandas

tba = gen.setup()

eventData = {}

for event in tba.events(2018):
    if event.event_type == 0:
        alliances = tba.event_alliances(event.key)
        
        for idx, alliance in enumerate(alliances):
            for team in alliance:
                print('memes')
        eventData[event] = []
        