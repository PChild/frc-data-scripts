import sys
import tbapy
import json
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

def matchResult(team, match):
    teamColor = 'blue'
    result = 'loss'
    
    if 'frc' not in str(team):
        team = 'frc' + str(team)
    
    if str(team) in match['alliances']['red']['team_keys']:
        teamColor = 'red'
        
    if match['winning_alliance'] == teamColor:
        result = 'win'
    
    if match['winning_alliance'] == '':
        result = 'tie'
    
    return result 

def progressBar(value, endvalue, bar_length=20):
        '''
        Simple progress bar

        :param value: The current progress level.
        :param endvalue: The max for the progress bar.        
        '''

        percent = float(value) / endvalue
        arrow = '-' * int(round(percent * bar_length)-1) + '>'
        spaces = ' ' * (bar_length - len(arrow))

        sys.stdout.write("\rPercent: [{0}] {1}%".format(arrow + spaces, int(round(percent * 100))))
        sys.stdout.flush()
        
def listOfDictToCSV(filename, listObj, colOrder=None):
    '''
    Saves a list of flat dictionaries out to a csv.
    
    :param filename: The file to write to
    :param listObj: The list of objects to write out
    :param colOrder: An array specifying the order to write columns in.
    '''
    
    f = open(filename + ".csv", 'w', encoding='utf-8')
    
    keys = listObj[0].keys()

    if colOrder:
        keys = colOrder
    
    for (idx, prop) in enumerate(keys):
        tail = ", "
        
        if idx == len(keys) - 1:
            tail = ""
            
        f.write(prop + tail)
    f.write("\n")
    
    for team in listObj:
        for (idx, prop) in enumerate(keys):
            tail = ", "
            
            if idx == len(keys) - 1:
                tail = ""
                
            f.write(str(team[prop]) + tail)
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