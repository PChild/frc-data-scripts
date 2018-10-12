import pandas as pd
import json

eloData = pd.read_csv('2018_Elo_end.csv')
regionTeams = json.load(open('teamRegionMapping.json'))

outFile = '2018 Region Elo Ratings.xlsx'
writer = pd.ExcelWriter(outFile)
fullList = []

for region in regionTeams:
    regionData = []
    for team in regionTeams[region]:
        teamNumber = int(team[3:])
        teamData = eloData[eloData.Team == teamNumber]
        if not teamData.empty:
            teamElo = teamData['Elo'].values[0]
            fullList.append((teamNumber, teamElo, region))
            regionData.append((teamNumber, teamElo))
    pd.DataFrame(regionData, columns=['Team', 'Elo']).sort_values(by='Elo', ascending=False).to_excel(writer, region, index=False)
pd.DataFrame(fullList, columns=['Team', 'Elo', 'Region']).sort_values(by='Elo', ascending=False).to_excel(writer, 'Full Data', index=False)
allData = writer.book.worksheets_objs.pop()
writer.book.worksheets_objs.sort(key=lambda x: x.name)
writer.book.worksheets_objs.insert(0, allData)
writer.save()