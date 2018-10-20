from robobrowser import RoboBrowser
from multiprocessing import Pool

baseURL = 'https://www.chiefdelphi.com/forums/memberlist.php?do=getall&page='
options = '&pp=100&order=asc&sort=username&lastpostafter=2018-01-01'

def getPageCount():
    browser = RoboBrowser(parser='html.parser', history=True)
    browser.open(baseURL + str(1) + options)
    
    #Find the vbulletin menu items, the page counter is one of these.
    menuControls = browser.find_all('td', {'class': 'vbmenu_control'})
    
    #Don't assume we got a valid menu control to make sure this breaks if CD changes
    #Iterage over them until we find something like 'Page 1 of 500' and save the last #
    pageCount = None
    for idx, entry in enumerate(menuControls):
        if 'Page 1 of ' in entry.text:
            pageCount = int(entry.text.split(' ')[-1])
            break
        
    return pageCount

def getUserAge(uid):
    browser = RoboBrowser(parser='html.parser', history=False)
    
    url = 'https://www.chiefdelphi.com/forums/member.php?u=' + str(uid)
    browser.open(url)
    
    
    #Iterate over the td elements, the lowest level one should have two children
    #a strong tag and a br tag. Find the text after br tag, strip off bs.
    #Make sure it's numeric to prevent getting bad data
    age = None
    for td in browser.find_all('td'):
        if 'Age' in td.text and len(td.findChildren()) == 2:
            ageVal = td.find('br').next.strip()
            
            if ageVal.isdigit():
                age = int(ageVal)
    return age
    

def processPage(pageVal):
    ageValues = []
    noAgeCount = 0
    
    browser = RoboBrowser(parser='html.parser')
    browser.open(baseURL + str(pageVal) + options)
    
    #in here find all the user rows and then fire off getUserAge calls
    #track how many 'none' values we get, log the ages.

def main():
    pageCount = getPageCount()
    print(pageCount)
    

if __name__ == '__main__':
    main()