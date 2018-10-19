from robobrowser import RoboBrowser

browser = RoboBrowser(history=True)
browser.open('https://www.chiefdelphi.com/forums/memberlist.php')

searchLink = browser.get_link('Search Members')
browser.follow_link(searchLink)

searchForm = browser.get_forms()[1]
searchForm['lastpostafter'].value = '2018-01-01'
searchForm['pp'].value = 100

browser.submit_form(searchForm)