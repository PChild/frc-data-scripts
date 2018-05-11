import requests, geocoder
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning

headers = {'X-TBA-App-Id': 'pchild:cdUsers:401'}
currentTime = datetime.now().strftime("%Y/%m/%d %H:%M")
pd.options.mode.chained_assignment = None
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def getTeamData(teamNumber):
    print('Getting events for team ' + str(teamNumber))
    teamEventsUrl = 'http://www.thebluealliance.com/api/v2/team/frc'+ str(teamNumber) +'/2017/events'
    teamEventsReq = requests.get(teamEventsUrl, headers = headers, verify=False)
    rank = 0
    eventCount = 0
    totalEvents = 0
    try:
        teamEventsData = teamEventsReq.json()
        print('Getting ranking data')
        totalEvents = len(teamEventsData)
        for event in teamEventsData:
            try:
                teamRankUrl = 'http://www.thebluealliance.com/api/v2/event/2017' + event['event_code'] + '/rankings'
                teamRankReq = requests.get(teamRankUrl, headers = headers, verify=False)
                teamRankData = teamRankReq.json()
                
                for rankPos in teamRankData:
                    if rankPos[1] == teamNumber:
                        percentRank = rankPos[0] / len(teamRankData)
                        rank = rank + percentRank
                        eventCount = eventCount + 1
            except:
                pass
    except:
        pass
    if eventCount == 0:
        eventCount = 1
    averageRank = rank / eventCount
    return [averageRank, totalEvents]

def getChiefUserInfo(uid, newUser):
    cdUserPage = requests.get('https://www.chiefdelphi.com/forums/member.php?u='+str(uid), verify=False)
    userSoup = BeautifulSoup(cdUserPage.content, "lxml")
    
    userName = userSoup.find(class_='bigusername').text.strip()
    postCount = int(userSoup.find(string='Posts').parent.parent.find('strong').text.replace(',', ''))
    
    try:
        teamNumber = int(userSoup.find(string='Team#').parent.parent.a['href'].split('/')[-1])
    except:
        teamNumber = 0
    teamRank, eventCount = getTeamData(teamNumber)
    
    if newUser:
        joinDate = userSoup.find(string='Forum Info').parent.parent.parent.strong.text
        print(userName + " is new!")
        isDistrict = checkDistrict(teamNumber)
        teamLat, teamLng = getTeamLoc(teamNumber) 
        try:
            role = userSoup.find(string='Team Role').parent.parent.text.split(':')[1].strip()
        except:
            role = ""
        try:
            age = int(userSoup.find(string='Age').parent.parent.text.split(':')[-1].strip())
        except:
            age = 0
        try:
            rookieYear = int(userSoup.find(string='Rookie Year').parent.parent.text.split(':')[-1].strip())
        except:
            rookieYear = 0          
    else:
        age = 0
        rookieYear = 0
        role = ""
        joinDate = ""
        teamLat = 0
        teamLng = 0
        isDistrict = False
    user = {'uid': uid,'userName': userName,'teamNum': teamNumber,'rookieYear': rookieYear,'role': role, 'postCount': postCount, 'joinDate': joinDate,'age': age,'lastSeen': currentTime,'seenCount': 1,'profileUrl': cdUserPage.url,'teamLat': teamLat,'teamLng': teamLng,'avgRank': teamRank, 'isDistrict': isDistrict, 'eventCount': eventCount}
    return user

def getTeamLoc(teamNumber):
    try:
        print("Geolocating team " + str(teamNumber))
        teamUrl = 'https://www.thebluealliance.com/api/v2/team/frc' + str(teamNumber)
        teamReq = requests.get(teamUrl, headers = headers, verify=False)
        teamData = teamReq.json()
        
        teamLocation = geocoder.google(teamData['location'])
        teamLat = teamLocation.lat
        teamLng = teamLocation.lng
        
    except:
        teamLat = 0
        teamLng = 0
    return [teamLat, teamLng]

def checkDistrict(teamNumber):
    try:
        districtUrl = 'https://www.thebluealliance.com/api/v2/team/frc' + str(teamNumber) + '/history/districts'
        districtReq = requests.get(districtUrl, headers = headers, verify=False)
        districtData = districtReq.json()
        
        isDistrict = bool(districtData)
    except:
        isDistrict = False
    return isDistrict
    
def main():
    xlsx = pd.ExcelFile('ChiefDelphiUsers.xlsx')
    df = pd.read_excel(xlsx, 'Users')
    
    cdPage = requests.get('http://www.chiefdelphi.com/forums/index.php', verify=False)
    soup = BeautifulSoup(cdPage.content, 'lxml')
    memberTableData = soup.find(id="collapseobj_forumhome_activeusers").tr.find(class_="alt1").find_all("a")
    
    for person in memberTableData:
        memberUid = int(person['href'].split("&")[1].replace("u=",""))
        newUser = df.loc[df['uid'] == memberUid].empty
        if newUser:
            userData = getChiefUserInfo(memberUid, True)
            df = df.append(userData, True)
        else:
            userData = getChiefUserInfo(memberUid, False)
            userIndex = df.loc[df['uid'] == memberUid].index[0]
            df['avgRank'][userIndex] = userData['avgRank']
            df['lastSeen'][userIndex] = currentTime
            df['seenCount'][userIndex] = df['seenCount'][userIndex] + 1
            df['postCount'][userIndex] = userData['postCount']
    df.to_excel('ChiefDelphiUsers.xlsx', sheet_name='Users')

if __name__ == "__main__":
    main()