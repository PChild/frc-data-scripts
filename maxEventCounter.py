import gen
from tqdm import tqdm
import slffFunctions as slff
#from tqdm import tqdm

tba = gen.setup()

normalEvents = [0, 1]

rookieVal = 7400
maxTeam = 7900
perPage = 500
pages = round(maxTeam / perPage)

yearStart = 2016
yearEnd = 2018

teamList = {}
eventList = {}
for year in range(yearStart, 2020):
    teamList[year] = gen.readTeamListCsv(year)['Teams'].tolist()
    eventList[year] = slff.fetchNormalEventData(year)
    

maxEvents = 0
maxTeam = ''
maxYear = 0
maxEventCodes = []
for team in tqdm(teamList[2019]):
    for year in range(yearStart, 2019):
        teamEvents = 0
        eventCodes = []
        eventDF = gen.readTeamCsv(team, 'events', year)
        if eventDF is not None:
            for event in eventDF['Event']:
                if event in eventList[year]:
                    eventCodes.append(event)
                    teamEvents += 1
            if teamEvents > maxEvents:
                maxEventCodes = eventCodes
                maxEvents = teamEvents
                maxTeam = team
                maxYear = year
print(maxEvents, maxTeam, year)
print(maxEventCodes)