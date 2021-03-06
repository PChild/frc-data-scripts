import tbapy
import json
import pandas as pd
from pathlib import Path
from git import Repo
import os
    
def setup(apiKey="TBA_KEY", useEnv=True):
    '''
    Sets up tbapy with an API key from a system environment variable    
    
    :param str apiKey: The TBA API key or system environment variable name for it
    :param bool useEnv: Set to True to fetch TBA API key from environment variable
    
    :return: Instance of TBA
    '''
    
    if useEnv:
        apiKey = os.getenv(apiKey)
    
    return tbapy.TBA(apiKey)

def getFirstAPI(apiKey='firstAPI'):
    return os.getenv(apiKey)

def readTeamCsv(key, dataType, year, names=None):
    key = teamString(key)
    repo = getRepoPath()
    return csvHandler(repo + 'teams/'+ str(year) + '/' + key + '/' + key + '_' + dataType +'.csv', names)
    
def readEventCsv(key, dataType, names=None, index=False):
    repo = getRepoPath()
    return csvHandler(repo + 'events/'+ key[:4] + '/' + key + '/' + key + '_' + dataType + '.csv', names, index)
    
def readTeamListCsv(year):
    repo = getRepoPath()
    return csvHandler(repo + 'teams/'+ str(year) + '/teams.csv', names=['Teams'])   

def teamEventMatches(team, event):
    team = teamString(team)
    res = None
    try:
        eM = readEventCsv(event, 'matches', names=['key', 'r1', 'r2', 'r3', 'b1', 'b2', 'b3', 'rScore', 'bScore'])
        res = eM[(eM.r1 == team) | (eM.r2 == team) | (eM.r3 == team) | (eM.b1 == team) | (eM.b2 == team) | (eM.b3 == team)]
    except:
        try:
            res = matchAdapter(team, event)
        except Exception as e:
            print("Error fetching team event matches for ", event)
    return res

def matchAdapter(team, event):
    tba = setup()
    tbaMatches = tba.team_matches(team, event)
    
    matchesList = []
    for match in tbaMatches:
        matchesList.append({'key': match['key'],
                        'r1': match['alliances']['red']['team_keys'][0],
                        'r2': match['alliances']['red']['team_keys'][1],
                        'r3': match['alliances']['red']['team_keys'][2],
                        'b1': match['alliances']['blue']['team_keys'][0],
                        'b2': match['alliances']['blue']['team_keys'][1],
                        'b3': match['alliances']['blue']['team_keys'][2],
                        'rScore': match['alliances']['red']['score'],
                        'bScore': match['alliances']['blue']['score']})
    return pd.DataFrame(matchesList)
    
    

def csvHandler(path, names, index=None):
    filePath = Path(path)    
    res = None    
    if filePath.exists():
        if filePath.stat().st_size > 0:
            res = pd.read_csv(path, names=names, skipinitialspace=True, index_col=index)
    return res

def teamString(team):
    if 'frc' not in str(team):
        team = 'frc' + str(team)
    return team
    
def teamNumber(team):
    if str(team)[:3] == "frc":
        team = str(team)[3:]
    return int(team)

def matchResult(team, match, useTba=False):
    team = teamString(team)
    if useTba == True:
        onRed = team in match['alliances']['red']['team_keys']
        onBlue = not onRed 
        redWins = match['winning_alliance'] == 'red'
        blueWins = match['winning_alliance'] == 'blue' 
        isTie = match['winning_alliance'] == ''
    else:
        onRed = (match['r1'] == team) or (match['r2'] == team) or (match['r3'] == team)
        onBlue = not onRed
        redWins = match['rScore'] > match['bScore']
        blueWins = match['bScore'] > match['rScore']
        isTie = match['rScore'] == match['bScore']
    
    if isTie:
        return 'TIE'
    elif (onBlue and blueWins) or (onRed and redWins):
        return 'WIN'
    else:
        return 'LOSS'

def listToCSV(filename, listObj):
    f = open(filename + ".csv", 'w', encoding='utf-8')
    
    for item in listObj:
        f.write(str(item) + "\n")
    f.close()
    
    
def listOfDictToCSV(filename, listObj, colOrder=None, header=True):
    '''
    Saves a list of flat dictionaries out to a csv.
    
    :param filename: The file to write to
    :param listObj: The list of objects to write out
    :param colOrder: An array specifying the order to write columns in.
    :param header: Whether to include header row
    '''
    
    f = open(filename + ".csv", 'w', encoding='utf-8')
    
    keys = listObj[0].keys()

    if colOrder:
        keys = colOrder
    
    if header:
        for (idx, prop) in enumerate(keys):
            tail = ","
            
            if idx == len(keys) - 1:
                tail = ""
                
            f.write(prop + tail)
        f.write("\n")
    
    for item in listObj:
        for (idx, prop) in enumerate(keys):
            tail = ","
            
            if idx == len(keys) - 1:
                tail = ""
                
            f.write(str(item[prop]) + tail)
        f.write("\n")
    f.close()
    
def writeJsonFile(filename, dictionary):
    '''
    Writes a dictionary to a JSON file
    
    :param filename: The file to write to
    :param dictionary: The dictionary to write out
    '''
    with open(filename + '.json', 'w') as outfile:
        json.dump(dictionary, outfile)
        
def updateRepoData(file, repoData):
    if file is None:
        file = 'repoSettings.csv'
        
    pd.DataFrame([repoData], columns=['Repo']).to_csv(file, index=False)
    
def getRepoPath(file=None):
    if file is None:
        file = 'repoSettings.csv'
        
    defaultRepoLocation = '../tba/'
    if not Path(file).exists():
        updateRepoData(file, defaultRepoLocation)

    return pd.read_csv(file)['Repo'].values[0]     

def handleRepo():
    tbaPath = getRepoPath()
    tbaGitUrl = 'https://github.com/the-blue-alliance/the-blue-alliance-data.git'
    tbaDir = Path(tbaPath)

    if not tbaDir.exists():
        tbaDir.mkdir()
    
    dotGitExists = Path(tbaPath + '.git/').exists()
    
    if dotGitExists:
        repo = Repo(tbaPath)        
        isBehind = (sum(1 for c in repo.iter_commits('master..origin/master')) > 0)
        
        if isBehind:
            repo.git.pull()
    
    if not dotGitExists:
        Repo.clone_from(tbaGitUrl, tbaPath)
    else:
        print('Up to date!')