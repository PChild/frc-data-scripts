import matplotlib.pyplot as plt
import pandas as pd
import gen

def generateData():
    eventData = []
    for val in range(1,25):
        eventData.append([])
    
    for event in tba.events(2018):
        if event['event_type'] == 0:
            alliances = tba.event_alliances(event['key'])
            distPoints = tba.event_district_points(event['key'])
            
            for allianceNum, alliance in enumerate(alliances):
                for pickNum, team in enumerate(alliance['picks']):
                    if pickNum == 0:
                        selectionPos = (allianceNum + 1) * 2 - 1
                    if pickNum == 1:
                        selectionPos = (allianceNum + 1) * 2
                    if pickNum == 2:
                        selectionPos = 24 - allianceNum
                    
                    teamPts = distPoints['points'][team]
                    eventData[selectionPos].append(teamPts['alliance_points'] + teamPts['elim_points'] + teamPts['qual_points'])
    return eventData

def readData():
    print('memes')

def main():
    #generateData()
    #readData()
    print('memes')

if __name__ == '__main__':
    tba = gen.setup()
    main()