import gen
import requests
import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup as bs

year = 2018
baseFolder = '..eventData/'

def saveUpdateDate(updateDate):
    gen.listToCSV('UpdateDate', [updateDate])
    
def getUpdateDate(year=2018):
    path = baseFolder + '/' + str(year) + '/UpdateDate.csv'
    raw = pd.read_csv(path)

def getSoup(endPoint):
    baseURL = 'https://frc-events.firstinspires.org/'+ str(year) + '/' 
    req = requests.get(baseURL + endPoint)
    return bs(req.content, "lxml")

def getEventTeams(event):
    soup = getSoup(event.upper())
    table = soup.find('table', id='teamtable')
    teamRows = table.find('tbody').find_all('tr')
    
    return [row.find('a').text for row in teamRows]

def getUpdateDate(soup=None):
    if soup is None:
        soup = getSoup('events')
    
    baseString = soup.find('div', class_='col-md-12').br.next_sibling.next_sibling
    return baseString[31:][:-28]
    
def getEventsData():
    soup = getSoup('events')   
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

def getAllEventTeams():
    eventsData = getEventsData()
    
    for event in eventsData:
        eventTeams = getEventTeams(event['Event Code'])