import gen
import pandas as pd
from tqdm import tqdm

tba = gen.setup()

events = tba.events(2018)

officialEvents = []

for event in events:
    if event['event_type'] in range(0, 10):
        officialEvents.append(event['key'])
        
eventAutoData = []
for event in tqdm(officialEvents):
    autoWinCount = 0
    matchCount = 0
    
    for match in tba.event_matches(event):
        autoWinner = ''
        
        redAuto = match['score_breakdown']['red']['autoScaleOwnershipSec']
        blueAuto = match['score_breakdown']['blue']['autoScaleOwnershipSec']
    
        if redAuto > blueAuto:
            autoWinner = 'red'
            matchCount += 1
        elif blueAuto > redAuto:
            autoWinner = 'blue'
            matchCount += 1
            
        if autoWinner == match['winning_alliance'] and autoWinner != '':
            autoWinCount += 1
    
    eventAutoData.append({'Event': event, 'Auto Win': autoWinCount, 'Matches': matchCount})
    
eventData = pd.DataFrame(eventAutoData)
eventData['% Win'] = eventData['Auto Win'] / eventData['Matches']
eventData.sort_values('% Win', ascending=False).to_csv('AutoWinData.csv', index=False)