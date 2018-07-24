from multiprocessing import Pool
from functools import partial
from pathlib import Path
import pandas as pd
import gen

tba = gen.setup()

def saveEventInfo(event):
    filePath = './tba/events/' + event[:4] + '/' + event + '/'
    fileName = event + '_info'
    fullPath = filePath + fileName
    outputPath = Path(filePath)
    outputFile = Path(fullPath + '.csv')
    
    if not outputPath.exists():
        outputPath.mkdir()
    
    if not outputFile.exists():
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
    filePath = './tba/events/' + event[:4] + '/' + event + '/'
    fileName = event + '_rankings'
    fullPath = filePath + fileName
    outputPath = Path(filePath)
    outputFile = Path(filePath + '.csv')
    
    if not outputPath.exists():
        outputPath.mkdir()
    
    if not outputFile.exists():
        try:
            rawRanks = tba.event_rankings(event)['rankings']
            
            ranksData = [{'Rank': entry['rank'], 'Team': entry['team_key']} for entry in rawRanks]
            colOrder = ['Rank','Team']
            gen.listOfDictToCSV(fullPath, ranksData, colOrder)
        except Exception as e:
            print(e)

def saveEventOPRs(event):
    filePath = './tba/events/' + event[:4] + '/' + event + '/' + event + '_opr'
    outputFile = Path(filePath + '.csv')
    
    if not outputFile.exists():
        try:
            rawRanks = tba.event_oprs(event)['oprs']
            
            oprData = sorted([{'OPR': rawRanks[team], 'Team': team} for team in rawRanks], key = lambda k: k['OPR'], reverse=True)
            colOrder = ['OPR', 'Team']
            gen.listOfDictToCSV(filePath, oprData, colOrder)
        except:
            pass

def saveTeamList(year):
    filePath = './tba/teams/' + str(year) + '/teams'
    outputFile = Path(filePath + '.csv')
    
    if not outputFile.exists():
        try:
            teams = []
            for page in range(0,16):
                teams += tba.teams(page, year, False, True)

            gen.listToCSV(filePath, teams)
        except Exception as e:
            print(e)    
    
def saveTeamEvents(year, team):
    filePath = './tba/teams/' + str(year) + '/' + team + '/'
    fileName = team + '_events'
    fullPath = filePath + fileName
    outputPath = Path(filePath)
    outputFile = Path(fullPath + '.csv')
    
    if not outputPath.exists():
        outputPath.mkdir()
    
    if not outputFile.exists():
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
    filePath = './tba/teams/' + str(year) + '/' + team + '/'
    fileName = team + '_awards.csv'  
    fullPath = filePath + fileName
    
    outFile = Path(fullPath)    
    
    if outFile.exists():
        outFile.unlink()
    

def saveTeamAwards(year, team):
    filePath = './tba/teams/' + str(year) + '/' + team + '/'
    fileName = team + '_awards'  
    fullPath = filePath + fileName
        
    outputPath = Path(filePath)
    outputFile = Path(fullPath + '.csv')
    

    eventData = pd.read_csv('tba/teams/' + str(year) + '/' + team + '/' + team + '_events.csv')
    
    if not outputPath.exists():
        outputPath.mkdir()
    
    if not outputFile.exists():
        try:
            teamYearAwards = []
            for event in eventData['Event']:
                evAwards = pd.read_csv('tba/events/' + str(year) + '/' + event + '/' + event + '_awards.csv', index_col=False, names=['Award', 'Name', 'Team'])
                teamAwards = evAwards[evAwards.Team == team]
                
                for idx, row in teamAwards.iterrows():
                    awardType = row['Award'].split('_')[1]
                    awardName = row['Name']
                    teamYearAwards.append({'Event': event, 'Type': awardType, 'Name': awardName})
            colOrder = ['Event', 'Type', 'Name']
            gen.listOfDictToCSV(fullPath, teamYearAwards, colOrder)
        except Exception as e:
            print(e)

def removeThenSaveAwards(year, team):
    removeTeamAwards(year, team)
    saveTeamAwards(year,team)

def main():
    pool = Pool()
    #pool.map(saveTeamList, range(1992, 2019))
    
    for year in range(1992, 2019):
        print("On year", year)
        #eventList = tba.events(year, False, True)
        #pool.map(saveEventRankings, eventList)
        #pool.map(saveEventOPRs, eventList)
        #pool.map(saveEventInfo, eventList)

        #df = pd.read_csv('tba/teams/' + str(year) + '/teams.csv', names=['Teams'])
        #pool.map(partial(removeThenSaveAwards, year), df['Teams'])
    pool.close()
    pool.join()
    
if __name__ == "__main__":
    main()