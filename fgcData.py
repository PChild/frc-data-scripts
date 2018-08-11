import gen
from bs4 import BeautifulSoup
import requests

def fetchYearTeams(year):
    raw = requests.get('https://first.global/'+ str(year) +'-nations/')
    soup = BeautifulSoup(raw.content, "lxml")
    articles = soup.find_all('article')
    
    baseList = []
    finalList = []
    for article in articles:
        link = article.find('a')
        name = link.get('title')
        url = link.get('href')
        
        if name not in baseList:
            baseList.append(name)
            
            cleanedName = name.replace('Team ', '').replace(' '+str(year), '')
            finalList.append({'Team': cleanedName, 'Link': url})

    return finalList

teams2018 = fetchYearTeams(2018)
teams2017 = fetchYearTeams(2017)

names2017 = [team['Team'] for team in teams2017]
for team in teams2018:
    in2017 = team['Team'] in names2017
    
    team['In 2017'] = ''
    if in2017:
        team['In 2017'] = 'Yes'


teams2018 = sorted(teams2018, key = lambda k: k['Team'])
gen.listOfDictToCSV('FGC 2018 Teams', teams2018, ['Team', 'Link', 'In 2017'])