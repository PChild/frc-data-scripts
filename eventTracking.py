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
    gen.listToCSV(baseFolder + str(year) + '/UpdateDate', [updateDate])
    
def getEventsUpdateDate(year=2018):
    path = baseFolder + '/' + str(year) + '/UpdateDate.csv'
    return pd.read_csv(path)

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
    prevDate = getEventsUpdateDate()
    
    if prevDate != currentDate:
        saveUpdateDate(currentDate)
        newData = getEventsData(eventSoup)
        oldData = readEventsData()
        
        added, lost, shared = getEventsDataUpdate(newData, oldData)
        saveEventData(added, lost, shared)
        saveEventsData(newData)
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
        #The try / except structure here is to handle the empty set case.
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

def getEventsDataUpdate(new, old=[{}]):    
    oldDict = transformEventsListToDict(old)
    newDict = transformEventsListToDict(new)
    
    added = []
    shared = []
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
    return [added, lost, shared]

def writeEventsUpdateReport(added, lost, shared):
    for events in added:    
        print('memems')
    #TODO make this work

def saveEventData(added, lost, shared):
    for group in [added, lost, shared]:
        for event in group:
            writeEventData(event)
            
def saveEventsData(data):
    gen.listOfDictToCSV(baseFolder + str(year) + '/CurrentEventsData', data)
    
def readEventsData():
    return pd.read_csv(baseFolder + str(year) + '/CurrentEventsData.csv').to_dict('records')

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