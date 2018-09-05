import gen
import requests
import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup as bs

year = 2018
baseFolder = '../eventData/'
updatesPath = 'eventsUpdates/'

def prepYear(year=2018):
    prepFolder(baseFolder)
    prepFolder(baseFolder + str(year))

def prepFolder(folder):
    folder = Path(folder)
    
    if not folder.exists():
        folder.mkdir()
    return folder

def getFolderFiles(folder):
    files = []
    
    for item in folder.iterdir():
        if item.is_file():
            files.append(item)
    return files

def saveUpdateDate(updateDate):
    gen.listToCSV('UpdateDate', [updateDate])
    
def getUpdateDate(year=2018):
    path = baseFolder + '/' + str(year) + '/UpdateDate.csv'
    raw = pd.read_csv(path)

def getSoup(endPoint='events'):
    baseURL = 'https://frc-events.firstinspires.org/'+ str(year) + '/' 
    req = requests.get(baseURL + endPoint)
    return bs(req.content, "lxml")

def getEventTeams(event):
    soup = getSoup(event.upper())
    table = soup.find('table', id='teamtable')
    teamRows = table.find('tbody').find_all('tr')
    
    return [row.find('a').text for row in teamRows]

def updateEventsData():
    eventSoup = getSoup()
    
    currentDate = getCurrentDate(eventSoup)
    prevDate = getUpdateDate()
    
    if prevDate != currentDate:
        eventsData = getEventsData(eventSoup)
    else:
        print('Events Data was up to date already')

def getCurrentDate(soup=None):
    if soup is None:
        soup = getSoup()
    baseString = soup.find('div', class_='col-md-12').br.next_sibling.next_sibling
    return baseString[31:][:-28]

def transformEventsListToDict(eventsList):
    eventsDict = {}
    for event in eventsList:
        try:
            eventsDict[event['Event Code']] = event
        except:
            pass
    return eventsDict

def getEventsData(soup=None):
    if soup is None:
        soup = getSoup()   
    eventRows = soup.find('table').tbody.find_all('tr')
    
    eventData = []
    for event in eventRows:
        cells = event.find_all('td')
        eventCode = cells[0].text
        
        weekData = cells[1].text.split(' ')
        eventWeek = weekData[0]
        eventStart = weekData[1]
        eventEnd = weekData[3]
        
        capacity = cells[3].text
        filled = cells[4].text
        avail = cells[5].text
        
        eventData.append({'Event Code': eventCode,
                          'Week': eventWeek,
                          'Start Date': eventStart,
                          'End Date': eventEnd,
                          'Capacity': capacity,
                          'Filled': filled,
                          'Available': avail})
    
    return eventData

def saveEventsDataUpdate(new, old=[{}]):    
    oldDict = transformEventsListToDict(old)
    newDict = transformEventsListToDict(new)
    
    added = []
    shared = [] #list of shared event codes
    for event in newDict:
        if event not in oldDict:
            added.append(newDict[event])
        else:
            shared.append(newDict[event])
    
    lost = []
    for event in old:
        if event not in newDict:
            lost.append(oldDict[event])
            
    for event in shared:
        prev = oldDict[event] 
        curr = newDict[event]
        
        weekDiff =  prev['Week'] != curr['Week']
        shared[event]['Week Change'] = prev['Week'] + ' -> ' + curr['Week'] if weekDiff else ''
            
        capDiff = curr['Capacity'] - prev['Capacity']
        shared[event]['Capacity Change'] = capDiff if capDiff != 0 else ''
        
        filledDiff = curr['Filled'] - prev['Filled']
        shared[event]['Filled Change'] = filledDiff if filledDiff != 0 else ''
        
        availDiff = curr['Available'] - prev['Available']
        shared[event]['Available Change'] = availDiff if availDiff != 0 else ''
        
        startDiff = curr['Start Date'] != prev['Start Date']
        shared[event]['Start Change'] = prev['Start Date'] + ' -> ' + curr['Start Date'] if startDiff else ''
        
        endDiff = curr['End Date'] != prev['End Date']
        shared[event]['End Change'] = prev['End Date'] + ' -> ' + curr['End Date'] if endDiff else ''

    for event in lost:
        for prop in ['Week', 'Start Date', 'End Date']:
            event[prop] = 'LOST'
        
        for prop in ['Week', 'Start', 'End']:
            event[prop + ' Change'] = 'LOST'
        
        for prop in ['Capacity', 'Available', 'Filled']:
            event[prop + ' Change'] = event[prop] * -1
            event[prop] = 0
            
    for event in added:
        for prop in ['Week', 'Start', 'End']:
            event[prop + ' Change'] = 'ADDED'
        
        for prop in ['Capacity', 'Available', 'Filled']:
            event[prop + ' Change'] = event[prop]
            
    for group in [added, lost, shared]:
        for event in group:
            writeEventData(event)

def getLatestFile(folderPath):
    fileList = getFolderFiles(folderPath)
    
    ret = None
    if len(fileList) > 0:
        ret = fileList[-1].name
    return ret

def latestFileNumber(folderPath):
    latestFile = getLatestFile(folderPath)
    
    ret = 0
    if latestFile is not None:
        ret = int(latestFile.split('.')[0][-3:])
    return ret
    
def writeEventData(event):
    prepYear()
    folderStr = baseFolder + str(year) + '/' + event['Event Code'] + '/'
    folderPath = prepFolder(folderStr)
    newNumber = latestFileNumber(folderPath) + 1
    fileStr = folderStr + 'EventData' + str(newNumber).zfill(3)
    keys = event.keys()
    gen.listOfDictToCSV(fileStr, [event], keys)

def getAllEventTeams():
    eventsData = getEventsData()
    
    for event in eventsData:
        eventTeams = getEventTeams(event['Event Code'])