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

def saveEventAwards(event):
    year = event[:4]
    basePath = '..\\tba\\events\\' + year + '\\'
    eventAwards = tba.event_awards(event)
    
    awardsData = []
    if eventAwards: 
        for award in eventAwards:
            for idx, recip in enumerate(award['recipient_list']):
                awardsData.append({'awardString': event + '_' + str(award['award_type']),
                                   'awardName': award['name'],
                                   'awardTeam': award['recipient_list'][idx]['team_key'],
                                   'awardPerson': award['recipient_list'][idx]['awardee']})
        
        colOrder = ['awardString', 'awardName', 'awardTeam', 'awardPerson']
        gen.listOfDictToCSV(basePath + event + '\\' + event + '_awards', awardsData, colOrder, False)

def saveEventAlliances(event):
    fileExists, fullPath = filePathHandler('events', event, 'alliances')

    alliances = []
    try:
        eventAlliances = tba.event_alliances(event)
    
        for alliance in eventAlliances:
            alliances.append({'Captain': alliance['picks'][0],
                             'First': alliance['picks'][1],
                             'Second': alliance['picks'][2]})
        gen.listOfDictToCSV(fullPath, alliances, ['Captain', 'First', 'Second'], False)
    except:
       pass

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

def find(listObj, key, value):
    for idx, dictObj in enumerate(listObj):
        if dictObj[key] == value:
            return idx
    return None

def saveEventTeamList(event):
    fileExists, fullPath = filePathHandler('events', event, 'teams')
    
    if not fileExists:
        try:
            teams = []
            matches = tba.event_matches(event)
            if len(matches) > 0:
                for match in matches:
                    for team in match['alliances']['red']['team_keys']:
                        if find(teams, 'Teams', team) is None:
                            teams.append({'Teams': team})
                    for team in match['alliances']['blue']['team_keys']:
                        if find(teams, 'Teams', team) is None:
                            teams.append({'Teams': team})
            else:
                for team in tba.event_teams(event, False, True):
                    teams.append({'Teams': team})
            gen.listOfDictToCSV(fullPath, teams)
        except Exception as e:
            print(e)

def removeEventTeamList(event):
    fileExists, fullPath = filePathHandler('events', event, 'teams')
    
    outFile = Path(fullPath + '.csv')    
    
    if fileExists:
        outFile.unlink()
 
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

def removeEventRanks(event):
    fileExists, fullPath = filePathHandler('events', event, 'rankings', int(event[:4]))
    outFile = Path(fullPath + '.csv')    
    
    if fileExists:
        outFile.unlink()

def removeTeamAwards(year, team):
    fileExists, fullPath = filePathHandler('teams', team, 'awards', year)
    outFile = Path(fullPath + '.csv')    
    
    if fileExists:
        outFile.unlink()
    
def saveTeamAwards(year, team):
    fileExists, fullPath = filePathHandler('teams', team, 'awards', year)    
    eventData = gen.readTeamCsv(team, 'events', year)
    
    if not fileExists:
        try:
            teamYearAwards = []
            for event in eventData['Event']:
                awardsExist, awardsPath = filePathHandler('events', event, 'awards')

                if awardsExist:
                    evAwards = pd.read_csv(awardsPath +'.csv', index_col=False, names=['Award', 'Name', 'Team'])
                    evAwards.Team = evAwards.Team.str.strip()
                    
                    if type(evAwards['Team'][0]) is not str:
                        evAwards['Team'] = 'frc' + evAwards['Team'].astype(str)
                    
                    teamAwards = evAwards[evAwards.Team == team]
                    
                    for idx, row in teamAwards.iterrows():
                        awardType = row['Award'].split('_')[1]
                        awardName = row['Name']
                        teamYearAwards.append({'Event': event, 'Type': awardType, 'Name': awardName})
            colOrder = ['Event', 'Type', 'Name']
            gen.listOfDictToCSV(fullPath, teamYearAwards, colOrder, False)
        except Exception as e:
            print(e)

def removeThenSaveTeamAwards(year, team):
    removeTeamAwards(year, team)
    saveTeamAwards(year,team)

def removeThenSaveEventRanks(event):
    removeEventRanks(event)
    saveEventRankings(event)

def main():
    startYear = 2019
    endYear = 2019
    pool = Pool()
    #pool.map(saveTeamList, range(startYear, endYear + 1))
    
    for year in range(startYear, endYear + 1):
        print("On year", year)
        #eventList = tba.events(year, False, True)
        #pool.map(saveEventAlliances, eventList)
        #pool.map(saveEventTeamList, eventList)
        #pool.map(saveEventRankings, eventList)
        #pool.map(removeThenSaveEventRanks, eventList)
        #pool.map(saveEventOPRs, eventList)
        #pool.map(saveEventInfo, eventList)
        #pool.map(saveEventAwards, eventList)

        teamList = gen.readTeamListCsv(year)
        #pool.map(partial(saveTeamEvents, year), teamList['Teams'])
        #pool.map(partial(saveTeamAwards, year), teamList['Teams'])
        pool.map(partial(removeThenSaveTeamAwards, year), teamList['Teams'])
        #pool.map(partial(saveTeamYearMatches, year), teamList['Teams'])
    pool.close()
    pool.join()
    
if __name__ == "__main__":
    main()