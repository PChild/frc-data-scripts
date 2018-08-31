import requests
from bs4 import BeautifulSoup as bs

year = 2018

def getSoup(endPoint):
    baseURL = 'https://frc-events.firstinspires.org/'+ str(year) + '/' 
    req = requests.get(baseURL + endPoint)
    return bs(req.content, "lxml")

def getEventTeams(event):
    soup = getSoup(event.upper())
    table = soup.find('table', id='teamtable')
    teamRows = table.find('tbody').find_all('tr')
    
    return [row.find('a').text for row in teamRows]

def getCapacityDate(soup=None):
    if soup is None:
        soup = getSoup('events')
    
    baseString = soup.find('div', class_='col-md-12').br.next_sibling.next_sibling
    return baseString[31:][:-28]
    
def getCapacityData():
    soup = getSoup('events')