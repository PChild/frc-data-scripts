from bs4 import BeautifulSoup
from tqdm import tqdm
import datetime
import requests
import gen

modUrl = 'https://www.chiefdelphi.com/forums/showgroups.php'
userUrl = 'https://www.chiefdelphi.com/forums/member.php?u='

firstAdder = 4
technicalAdder = 25
competitionAdder = 19
otherAdder = 18

def getChiefUserInfo(uid):
    cdUserPage = requests.get(userUrl + str(uid))
    userSoup = BeautifulSoup(cdUserPage.content, "lxml")
    
    postCount = int(userSoup.find(string='Posts').parent.parent.find('strong').text.replace(',', ''))
    
    try:
        teamNumber = int(userSoup.find(string='Team#').parent.parent.a['href'].split('/')[-1])
    except:
        teamNumber = 0
    try:
        rookieYear = int(userSoup.find(string='Rookie Year').parent.parent.text.split(':')[-1].strip())
    except:
        rookieYear = 0       
    lastActive = ''
    if len(userSoup.find_all('span', class_='time')) > 1:
        lastActive = userSoup.find_all('span', class_='time')[0].parent.text[15:-1]
    return [postCount, teamNumber, rookieYear, lastActive]

def processMod(inputRow):
    result = None
    
    cells = inputRow.find_all('td')

    isUserRow = len(cells[0].find_all('img')) > 0
    
    if isUserRow:
        userName = cells[1].text.strip()
        userID = cells[1].find('a', href=True)['href'].split('=')[2]
        
        postCount, teamNumber, rookieYear, lastActive = getChiefUserInfo(userID)
        
        forums = [link.text for link in cells[2].find_all('a')]
        forumCount = len(forums)
        forums = ' / '.join(forums)
        
        forumCount += ('FIRST' in forums) * firstAdder
        forumCount += ('Technical' in forums) * technicalAdder
        forumCount += ('Competition' in forums) * competitionAdder
        forumCount += ('Other' in forums) * otherAdder
        
        result = {'Username': userName, 'Forum Count': forumCount, 'Forums': forums, 'Post Count': postCount, 'Team Number': teamNumber, 'Rookie Year': rookieYear, 'Last Activity': lastActive}
        
    return result

now = datetime.datetime.now()
timeStamp = now.strftime("%Y-%m-%d")

r = requests.get(modUrl)
soup = BeautifulSoup(r.content,"html.parser")

modTable = soup.find_all('table')[7].find_all('tr')

modData = []
for row in tqdm(modTable):
    result = processMod(row)
    if result is not None:
        modData.append(result)
    
gen.listOfDictToCSV('cdMods-' + timeStamp, modData, ['Username', 'Forum Count', 'Post Count', 'Team Number', 'Rookie Year', 'Last Activity', 'Forums'])