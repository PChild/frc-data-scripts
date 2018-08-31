import gen
from tqdm import tqdm

tba = gen.setup()

def getEventSizes(year=2018):
    eventSizes = []
    print('Getting event sizes')
    for event in tqdm(tba.events(year)):
        if event['event_type'] == 0:
            eventSizes.append(len(tba.event_teams(event['key'], False, True)))
    return eventSizes

def saveRegionalData(year=2018):
    eventData = []
    print('Saving regional data')
    for event in tqdm(tba.events(year)):
        if event['event_type'] == 0:
            eventData.append({'Key': event['key'], 'Size': len(tba.event_teams(event['key'], False, True))})
    gen.listOfDictToCSV(str(year) + 'Regional Sizes', eventData)

def savedDraftSizeData(eventSizes):
    data = []    
    for teamCount in range(1, 26):
        draftSize = teamCount * 3
        multiTier = 0
        for event in eventSizes:
            multiTier += event < draftSize
        data.append({'SLFF Teams': teamCount, 'Multi-tier events': multiTier})
    gen.listOfDictToCSV('Draft Sizing', data)
    
def main():
    saveRegionalData()

if __name__ == '__main__':
    main()