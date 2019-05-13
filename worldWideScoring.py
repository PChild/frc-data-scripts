import gen
import eventTypes
import pandas as pd
import slffFunctions
from tqdm import tqdm

tba = gen.setup()
year = 2019

draftData = pd.read_excel('worldwideData.xlsx')
drafters = draftData.columns.tolist()[1:]

detroit = tba.event('2019cmpmi')
drafterScores = []

for drafter in tqdm(drafters):
    drafterData = {'Drafter': drafter, 'Total': 0}
    for i in range(1,4):
        drafterData['P' + str(i) + ' Pick'] = ''
        drafterData['P' + str(i) + ' Score'] = 0
    
    for idx, team in enumerate(draftData[drafter]):
        earliestEvent = detroit
        
        for event in tba.team_events(team, year):
            if event['start_date'] < earliestEvent['start_date']:
                if event['event_type'] in [eventTypes.DISTRICT, eventTypes.REGIONAL]:
                    earliestEvent = event
                
        playPoints = sum(slffFunctions.getPlayPoints('frc' + str(team), earliestEvent['key'])[0:3])
        awardPoints = slffFunctions.getAwardPoints(team, earliestEvent['key'])[0]
        
        teamPoints = playPoints + awardPoints
        
        drafterData['P' + str(idx + 1) + ' Team'] = team
        drafterData['P' + str(idx + 1) + ' Score'] =  teamPoints
        drafterData['Total'] += teamPoints
    drafterScores.append(drafterData)

drafterScores = sorted(drafterScores, key= lambda k: k['Total'], reverse=True)
cols = ['Drafter', 'Total', 'P1 Team', 'P1 Score', 'P2 Team', 'P2 Score', 'P3 Team', 'P3 Score']
gen.listOfDictToCSV(str(year) + ' World Wide Regional Scores', drafterScores, cols)