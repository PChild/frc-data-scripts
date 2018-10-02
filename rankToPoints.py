import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd
import gen

def generateData(datafile):
    eventData = []
    for val in range(0,24):
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
                    eventData[selectionPos - 1].append(teamPts['award_points'])
                    #eventData[selectionPos - 1].append(teamPts['alliance_points'] + teamPts['elim_points'] + teamPts['qual_points'])
    frame = pd.DataFrame(eventData).transpose()
    frame.to_csv(datafile)
    return frame

def readData(datafile):
    if Path(datafile).exists():
        return pd.read_csv(datafile, index_col=0)
    else:
        return generateData(datafile)

def main():
    data = readData('ranksData.csv')
    
    baseNames = data.columns
    nameMap = {}
    for val in baseNames:
        nameMap[val] = str(int(val) + 1)
    data = data.rename(index=str, columns=nameMap)
    
    ax = data.plot(kind='box', title='Award Points by Draft Position at 2018 FRC Regionals', figsize=(20,10))
    ax.set_xlabel('Draft Position')
    ax.set_ylabel('Award Points')
    
    plt.savefig('Award Points by Draft Position')

if __name__ == '__main__':
    tba = gen.setup()
    main()
