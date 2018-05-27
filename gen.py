import sys
import tbapy
import json
import os
    
def setup():
    return tbapy.TBA(os.getenv("TBA_KEY"))
    
def progressBar(value, endvalue, bar_length=20):

        percent = float(value) / endvalue
        arrow = '-' * int(round(percent * bar_length)-1) + '>'
        spaces = ' ' * (bar_length - len(arrow))

        sys.stdout.write("\rPercent: [{0}] {1}%".format(arrow + spaces, int(round(percent * 100))))
        sys.stdout.flush()
        
def listOfDictToCSV(filename, listObj):
    f = open(filename + "O.csv", 'w')

    for prop in listObj[0].keys():
        f.write(prop + ", ")
    f.write("\n")
    
    for team in listObj:
        for prop in team.keys():
            f.write(str(team[prop]) + ", ")
        f.write("\n")
    f.close()
    
def writeJsonFile(filename, dictionary):
    with open(filename + '.json', 'w') as outfile:
        json.dump(dictionary, outfile)