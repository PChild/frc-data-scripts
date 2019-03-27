import pandas
import requests
from io import StringIO 
import gen
from datetime import datetime
from dateutil import parser
import awardTypes
import eventTypes
from tqdm import tqdm
from statistics import mean
import copy

tba = gen.setup()

#General settings for running waiver stuff
year = 2019
teamKey = 'CHS'
maxDraftRounds = 12
currentWeek = 5

#Document and sheet specific url stuff, change for next year
bookID = '1-2Flli3g1d_r2sEkr0DjLnyXGgyn3LwC3uSh5uVThTc'
mainSheetID = '963745347'
distSheetID = '564274829'

#General g sheets url stuff.
baseURL = 'https://docs.google.com/spreadsheets/d/'
exportPart = '/export?format=csv&gid='

#Represent district plays as team to event pairs.
def buildDistTeamEventPairs(dist):
    distEvents = tba.district_events(dist)
    distTeams = [team[3:] for team in tba.district_teams(dist, False, True)]
    
    sortedEvents = sorted(distEvents, key= lambda event: event['week'])
    
    teamEventPairs = []
    print("Building team-event pair list")
    for event in tqdm(sortedEvents):
        if event['event_type'] == eventTypes.DISTRICT:
            eventTeams = [team[3:] for team in tba.event_teams(event['key'], False, True)]
            for team in eventTeams:
                #Handle out-of-district plays
                if team in distTeams:
                    alreadyIn = len([item for item in teamEventPairs if item[0] == team])
                    
                    if alreadyIn < 2:
                        teamEventPairs.append((team, event['key'], event['week']))
    
    return teamEventPairs

#Retrieves data on a team's in season performance to date.       
def getTeamData(team):
    teamInt = int(team)
    
    teamStruct = {'Team': teamInt,
                  'Wins': 0,
                  'Losses': 0,
                  'Ties': 0,
                  'Awards': "",
                  'OPR': [],
                  'Rank': [],
                  'Draft Pos': [],
                  'Events': 0}

    teamEvents = tba.team_events(teamInt, year)
    
    for event in teamEvents:
        if event['event_type'] in [eventTypes.REGIONAL, eventTypes.DISTRICT]:
            #if the event end date is before now then the team has played this event and we can get data for it
            if parser.parse(event['end_date']) < datetime.now():
                teamStruct['Events'] += 1
    
                eventAwards = tba.team_awards(teamInt, year, event['key'])
    
                for award in eventAwards:
                    dontCareAwards = [awardTypes.FINALIST, awardTypes.WINNER, awardTypes.DEANS_LIST, awardTypes.WOODIE_FLOWERS]
                    if award['award_type'] not in dontCareAwards:
                        teamStruct['Awards'] += award['name'] + ' / '
                        
                eventStats = tba.team_status(int(team), event['key'])
                teamStruct['Rank'].append(eventStats['qual']['ranking']['rank'])
                
                #quals win / loss / ties
                teamStruct['Wins'] += eventStats['qual']['ranking']['record']['wins']
                teamStruct['Losses'] += eventStats['qual']['ranking']['record']['losses']
                teamStruct['Ties'] += eventStats['qual']['ranking']['record']['ties']
                
                #elims win / loss / ties
                if eventStats['playoff']:
                    teamStruct['Wins'] += eventStats['playoff']['record']['wins']
                    teamStruct['Losses'] += eventStats['playoff']['record']['losses']
                    teamStruct['Ties'] += eventStats['playoff']['record']['ties']
                
                if eventStats['alliance']:
                    draftAlliance = eventStats['alliance']['number']
                    draftPick = eventStats['alliance']['pick']
                    draftNum = 24
                    
                    if draftPick < 2:
                         draftNum = draftAlliance * 2 + draftPick - 1
                    else:
                        draftNum = 25 - draftAlliance
                    teamStruct['Draft Pos'].append(draftNum)
                    
                teamStruct['OPR'].append(tba.event_oprs(event['key'])['oprs']['frc' + team])
    return teamStruct

#Pulls regional data from slff sheet, filters to only our tiers, removes drafted teams,
#and then saves out data on teams still available
def handleRegionals():
    #Get data from internet and read it in
    req = requests.get(baseURL + bookID + exportPart + mainSheetID)
    decodedData = StringIO(req.content.decode('utf-8'))
    dataDf = pandas.read_csv(decodedData,index_col=0)
    
    #Cleans up the sheet some so its less bad to work with.
    #Standardizes column names, resets tier being the index, drops crap columns,
    #removes null rows
    renameDict = {'index': 'Tier', 'event code': 'Code'}
    for val in range(0, maxDraftRounds + 1):
        if val > 3:
            renameDict['[Round ' + str(val) + ']'] = 'Rnd ' + str(val)
        else:
            renameDict['Round ' + str(val)] = 'Rnd ' + str(val)
            
    dataDf = dataDf.reset_index().rename(columns=renameDict).iloc[1:]
    trashCols = ['Livescorer data generator DO NOT EDIT', 'Unnamed: 3', 'Unnamed: 4',]
    dataDf = dataDf.drop(trashCols, axis=1)
    dataDf = dataDf[pandas.notnull(dataDf['Tier'])]

    #Build list of drafts we did
    draftsList = dataDf['Code'].unique().tolist()
    
    #Holds data on teams available for waiver
    availableTeams = []
    
    #Iterate over all the events we drafted
    for draftCode in draftsList: 
        
        #Handle regional events
        if str(year) in draftCode:
            
            eventStart = tba.event(draftCode)['start_date']
          
            #only get data for regionals that have not yet played
            if parser.parse(eventStart) > datetime.now():  
                print('Processing', draftCode)
                
                eventTeams = [team[3:] for team in tba.event_teams(draftCode, False, True)]
                
                #Only care about teams taken in our tier.
                slffTeamRows = dataDf[dataDf['Code'] == draftCode]
                ourTier = slffTeamRows[slffTeamRows['Player'] == teamKey]['Tier'].iloc[0]
                tierTeamRows = slffTeamRows[slffTeamRows['Tier'] == ourTier]
                
                for idx, draftResult in tierTeamRows.iterrows():
                    for draftRound in range(0, maxDraftRounds):
                        roundStr = 'Rnd ' + str(draftRound + 1)
                        teamVal = draftResult[roundStr]
                        
                        if not pandas.isnull(teamVal):
                            try:
                                eventTeams.remove(teamVal)
                            except:
                                print(draftResult['Player'], 'has MIA:', teamVal, '@', draftResult['Event'], '(' + draftCode + ')')
                
                #Now that we've removed all the drafted teams, lets collect data on our picks and available picks
                for team in tqdm(eventTeams):
                        teamData = getTeamData(team)
                        teamData['Code'] = draftCode
                        teamData['Tier'] = ourTier
                        teamData['Draft Name'] = tierTeamRows.iloc[0]['Event']
                        availableTeams.append(teamData)
            else:
                print("Skipping", draftCode, "it has already played")



    #Find averages of numeric stats
    for entry in availableTeams:    
        for item in ['OPR', 'Rank', 'Draft Pos']:
            out = '-'
            if len(entry[item]) > 0:
                out = mean(entry[item])
            entry['Avg '+ item] = out
    
    exportCols = ['Code', 'Draft Name', 'Tier', 'Team', 'Wins', 'Losses', 'Ties', 'Awards', 'Avg OPR', 'Avg Rank', 'Avg Draft Pos', 'Events']
    gen.listOfDictToCSV('Regional Waiver Data', availableTeams, exportCols)

def buildAvailPairs(distDf, dist):
    teamEventPairs = buildDistTeamEventPairs(str(year) + dist)
    takenPairs = []
    
    #filter the district data to only be the region we care about, remove empty columns
    #fill any nan with '-' to avoid dealing with it, filter to only columns that are team or event
    districtTakenRows = distDf.loc[dist].dropna(axis=1, how='all').fillna('-')
    dataCols = [item for item in districtTakenRows.columns.tolist() if '-' in item]
    distData = districtTakenRows[dataCols]
    
    #We need to iterate over the pairs in each row (ie col count / 2)
    itersNeeded = len(distData.columns) / 2
    
    #Iterate over each row, within it build tuples of taken team-event pairs
    for idx, row in distData.iterrows():
        i = 0
        while i < itersNeeded:
            startVal = i * 2
            endVal = i * 2 + 2
            
            pairSet = row.iloc[startVal:endVal].values
            takenPairs.append((pairSet[0], pairSet[1]))
            
            i += 1
            
    #Now that taken team-event pairs are built remove the taken ones from the
    #whole list to isolate available ones.
    filteredPairSet = copy.deepcopy(teamEventPairs)
    for pair in teamEventPairs:
        tmpPair = (pair[0], pair[1])
        if tmpPair in takenPairs:
            filteredPairSet.remove(pair)
    
    for pair in takenPairs:
        if pair[1] == '-':
            teamPairSets= [item for item in filteredPairSet if item[0] == pair[0]]
            weekSorted = sorted(teamPairSets, key= lambda item: item[2])
            if len(weekSorted) > 0:
                filteredPairSet.remove(weekSorted[0])
                
    tmpSet = copy.deepcopy(filteredPairSet)
    for pair in tmpSet:
        if pair[2] + 1 < currentWeek:
            filteredPairSet.remove(pair)
            
    return filteredPairSet

#Pull data from Justin's district sheet
def handleDistricts():
    req = requests.get(baseURL + bookID + exportPart + distSheetID)
    decodedData = StringIO(req.content.decode('utf-8'))
    distDf = pandas.read_csv(decodedData,index_col=0)
    distDf.columns = distDf.iloc[0].values
    distDf = distDf[1:]
    
    distKeys = distDf.index.unique().tolist()
    availTeams = []
    
    for dist in distKeys:
        print("Processing", dist)
        availPairs = buildAvailPairs(distDf, dist)
        for pair in availPairs:
            teamData = getTeamData(pair[0])
            teamData['Dist'] = dist
            availTeams.append(teamData)
            
    #Find averages of numeric stats
    for entry in availTeams:    
        for item in ['OPR', 'Rank', 'Draft Pos']:
            out = '-'
            if len(entry[item]) > 0:
                out = mean(entry[item])
            entry['Avg '+ item] = out
    
    exportCols = ['Dist', 'Team', 'Wins', 'Losses', 'Ties', 'Awards', 'Avg OPR', 'Avg Rank', 'Avg Draft Pos', 'Events']
    gen.listOfDictToCSV('Regional Waiver Data', availTeams, exportCols)
 
def main():
    #print('memes')
    #handleRegionals()
    handleDistricts()
    
if __name__ == '__main__':
    main()