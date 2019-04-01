import gen
import slffFunctions as slff
from tqdm import tqdm

tba = gen.setup()

normalEvents = [0, 1]

rookieVal = 7400
maxTeam = 7900
perPage = 500
pages = round(maxTeam / perPage)

yearStart = 2016
yearEnd = 2018
yearRange = range(yearStart, yearEnd + 1)

teamList = {}
eventList = {}
for year in yearRange:
    teamList[year] = gen.readTeamListCsv(year)['Teams'].tolist()
    eventList[year] = slff.fetchNormalEventData(year)

#teams = gen.readTeamListCsv(2019)['Teams'].tolist()
teams = tba.district_teams('2019tx', False, True)
#teams = ['frc125', 'frc401', 'frc7179']

eventFields = ['Code', 'Type', 'Week', 'Total Points', 'Award Points', 'Award Names', 'Draft Points', 'Rank Points', 'Elim Points', 'Rank']

teamData = {}
for team in tqdm(teams):
    teamData[team] = {}
    for year in yearRange:
        teamData[team][year] = []
        if team in teamList[year]:
            teamEvents = gen.readTeamCsv(team, 'events', year)
            for idx, event in teamEvents.iterrows():
                eventKey = event['Event']
                eventType = 'District' if event['Type'] == 1 else 'Regional'
                if eventKey in eventList[year]:
                    awardData = slff.getAwardPoints(team, eventKey)
                    playData = slff.getPlayPoints(team, eventKey)
                    totalPoints = sum(playData[:3]) + awardData[0]
                    eventDict = [eventKey, eventType, eventList[year][eventKey], totalPoints] + awardData + playData
                    eventPacket = {}
                    for idx, field in enumerate(eventFields):
                        eventPacket[field] = eventDict[idx]
                    teamData[team][year].append(eventPacket)

def prepFields():
    fields = ['Team']
    
    for num in range(1,5):
        for field in eventFields:
            fields.append(field + ' ' + str(num))
    return fields

def prepDict(team):
    blankDict = {}
    for field in prepFields():
        blankDict[field] = ''
    blankDict['Team'] = team[3:]
    return blankDict

for year in yearRange:
    yearData = []
    for team in teams:
        teamDict = prepDict(team)
        eventCounter = 0
        
        for event in sorted(teamData[team][year], key= lambda k: k['Week']):
            eventCounter += 1
            
            for field in event:
               key = field + ' ' + str(eventCounter) 
               teamDict[key] = event[field]
        yearData.append(teamDict)
    gen.listOfDictToCSV(str(year) + ' TX Data', yearData, prepFields())
        