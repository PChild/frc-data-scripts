from multiprocessing import Pool
from functools import partial
from pathlib import Path
import pandas as pd
import gen

tba = gen.setup()

def filePathHandler(teamsOrEvents, code=None, dataType=None, year=None):
    repo = gen.getRepoPath()
    if teamsOrEvents == 'events':
        year = code[:4]
    if teamsOrEvents == 'teams' and code == None:
        filePath = repo + 'teams/' + str(year) + '/'
        fileName = dataType
    else:
        filePath = repo + teamsOrEvents +'/' + str(year) + '/' + code + '/'
        fileName = code + '_' + dataType
    fullPath = filePath + fileName
    outputPath = Path(filePath)
    outputFile = Path(fullPath + '.csv')
    
    if not outputPath.exists():
        outputPath.mkdir()
        
    return [outputFile.exists(), fullPath]

def saveTeamYearMatches(year, team):
    fileExists, fullPath = filePathHandler('teams', team, 'matches', year)
    
    if not fileExists:
        try:
            teamEvents = gen.readTeamCsv(team, 'events', year)
            teamMatches = pd.concat(gen.teamEventMatches(team, event) for event in teamEvents['Event'])
            
            teamMatches.to_csv(fullPath + '.csv', index=False)
        except Exception as e:
            print(e)
        

def saveEventInfo(event):
    fileExists, fullPath = filePathHandler('events', event, 'info')

    if not fileExists:
        try:
            raw = tba.event(event)
            
            if not raw['start_date']:
                raw['start_date'] = event[:4] + '-12-31'
            
            eventData = [{'Type': raw['event_type'], 'Official': raw['event_type'] < 10 and raw['event_type'] >= 0, 'Start Date': raw['start_date']}]
            colOrder = ['Type', 'Official', 'Start Date']            
            gen.listOfDictToCSV(fullPath, eventData, colOrder)
        except Exception as e:
            print(e)

def saveEventRankings(event):
    fileExists, fullPath = filePathHandler('events', event, 'rankings')

    if not fileExists:
        try:
            rawRanks = tba.event_rankings(event)['rankings']
            
            ranksData = [{'Rank': entry['rank'], 'Team': entry['team_key']} for entry in rawRanks]
            colOrder = ['Rank','Team']
            gen.listOfDictToCSV(fullPath, ranksData, colOrder)
        except Exception as e:
            print(e)

def saveEventOPRs(event):
    fileExists, fullPath = filePathHandler('events', event, 'opr')
    
    if not fileExists:
        try:
            rawRanks = tba.event_oprs(event)['oprs']
            
            oprData = sorted([{'OPR': rawRanks[team], 'Team': team} for team in rawRanks], key = lambda k: k['OPR'], reverse=True)
            colOrder = ['OPR', 'Team']
            gen.listOfDictToCSV(fullPath, oprData, colOrder)
        except Exception as e:
            print(e)

def saveTeamList(year):
    fileExists, fullPath = filePathHandler('teams', None, 'teams', year)

    if not fileExists:
        try:
            teams = []
            for page in range(0,16):
                teams += tba.teams(page, year, False, True)

            gen.listToCSV(fullPath, teams)
        except Exception as e:
            print(e)    
    
def saveTeamEvents(year, team):
    fileExists, fullPath = filePathHandler('teams', team, 'events', year)
    
    if not fileExists:
        try:
            raw = tba.team_events(team, year)
            
            for idx, event in enumerate(raw):
                if not event['start_date']:
                    event['start_date'] = '9999-99' + str(idx)  
            
            data = sorted([{'Event': event['key'], 'Type': event['event_type'], 'Start Date': event['start_date']} for event in raw], key = lambda k: k['Start Date'])
            colOrder = ['Event', 'Type', 'Start Date']
            gen.listOfDictToCSV(fullPath, data, colOrder)
        except Exception as e:
            print(e)

def removeTeamAwards(year, team):
    fileExists, fullPath = filePathHandler('teams', team, 'awards', year)
    outFile = Path(fullPath)    
    
    if fileExists:
        outFile.unlink()
    
def saveTeamAwards(year, team):
    fileExists, fullPath = filePathHandler('teams', team, 'awards', year)    
    eventData = gen.readTeamCsv(team, 'events, year')
    
    if not fileExists:
        try:
            teamYearAwards = []
            for event in eventData['Event']:
                awardsExist, awardsPath = filePathHandler('events', event, 'awards')

                if awardsExist:
                    evAwards = pd.read_csv(awardsPath +'.csv', index_col=False, names=['Award', 'Name', 'Team'])
                    
                    if type(evAwards['Team'][0]) is not str:
                        evAwards['Team'] = 'frc' + evAwards['Team'].astype(str)
                    
                    teamAwards = evAwards[evAwards.Team == team]
                    
                    for idx, row in teamAwards.iterrows():
                        awardType = row['Award'].split('_')[1]
                        awardName = row['Name']
                        teamYearAwards.append({'Event': event, 'Type': awardType, 'Name': awardName})
            colOrder = ['Event', 'Type', 'Name']
            gen.listOfDictToCSV(fullPath, teamYearAwards, colOrder)
        except Exception as e:
            print(e)

def removeThenSaveTeamAwards(year, team):
    removeTeamAwards(year, team)
    saveTeamAwards(year,team)

def main():
    pool = Pool()
    #pool.map(saveTeamList, range(1992, 2019))
    
    for year in range(1992, 2019):
        print("On year", year)
        eventList = tba.events(year, False, True)
        #pool.map(saveEventRankings, eventList)
        pool.map(saveEventOPRs, eventList)
        pool.map(saveEventInfo, eventList)

        #teamList = gen.readTeamListCsv(year)
        #pool.map(partial(saveTeamYearMatches, year), teamList['Teams'])
    pool.close()
    pool.join()
    
if __name__ == "__main__":
    main()