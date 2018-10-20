from robobrowser import RoboBrowser
from multiprocessing import Pool
import time
import gen

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
    browser = RoboBrowser(parser='html.parser')
    
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
    usersProcessed = 0
    
    browser = RoboBrowser(parser='html.parser')
    browser.open(baseURL + str(pageVal) + options)
    
    #Find all the links on the page, if the href in a link has member.php in it then
    #it's a member link, so pull out the uid from it and add that uid to the list
    userIDs = [link['href'].split('u=')[1] for link in browser.find_all('a', href=True) if 'member.php?' in link['href']]
    usersProcessed = len(userIDs)
    
    for user in userIDs:
        age = getUserAge(user)
        time.sleep(1)
        noAgeCount += age is None
        
        if age is not None:
            ageValues.append(age)
            
    return [ageValues, noAgeCount, usersProcessed]

def main():
    #Record what time we start, figure out how many pages we're going to scrape,
    #and set the pool to run with 8 workers.
    start = time.time()
    pageCount = getPageCount()
    pool = Pool(processes=8)
    
    #resultSet will be a list of lists with each sublist containing the output
    #from processPage
    resultSet = pool.map(processPage, range(1, pageCount + 1))
    
    #This code just itereates through the result set and combines them
    ages = []
    noAgeCount = 0
    usersProcessed = 0
    for entry in resultSet:
        ages += entry[0]
        noAgeCount += entry[1]
        usersProcessed += entry[2]
        
    #Figure out how long the script took to run
    end = time.time()
    diff = round((end - start)/60,1)
    
    #Save the age data and then print some basic info 
    gen.listToCSV('CD-Ages-' + time.strftime('%Y-%m-%d'), ages)
    print(noAgeCount, 'out of', usersProcessed, 'had no age set. :(')
    print('Scraping run took', diff, 'minutes.')
    

if __name__ == '__main__':
    main()