import requests
from bs4 import BeautifulSoup
import gen
from tqdm import tqdm
import datetime

now = datetime.datetime.now()
timeStamp = now.strftime("%Y-%m-%d")

baseURL = 'https://www.chiefdelphi.com/forums/memberlist.php?&order=DESC&sort=reputation&pp=100&page='
pagesToFetch = 422


userRanks = []
for val in tqdm(range(1, pagesToFetch + 1)):
    r = requests.get(baseURL + str(val))
    soup = BeautifulSoup(r.content,"html.parser")
    userTable = soup.find_all("table", {"class":"tborder", "cellpadding": "6", 
                                    "cellspacing": "1", "border": "0", 
                                    "width": "100%", "align": "center"})[3]
    
    userRows = userTable.find_all('tr')
    
    for row in range(1, len(userRows) - 1):
        cells = userRows[row].find_all('td')
        
        rank = 100 * (val - 1) + row
        
        posts = int(cells[1].text.replace(",", ""))
        name = userRows[row].find('a').text
        comp = cells[3].text
        team = cells[4].text
        role = cells[5].text
        rookie = cells[6].text
        
        userRanks.append({'Rank': rank,
                          'User Name': name,
                          'Posts': posts,
                          'Competition': comp,
                          'Team': team,
                          'Role': role,
                          'Rookie Year': rookie})
    
colOrder = ['Rank', 'User Name', 'Posts', 'Competition', 'Team', 'Role', 'Rookie Year']
gen.listOfDictToCSV("cdRepRanks" + timeStamp, userRanks, colOrder)