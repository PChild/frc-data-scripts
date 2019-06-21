import requests
import gen

cdThread = 'https://www.chiefdelphi.com/t/concerns-about-an-off-season-event/358211.json'

data = [{'Person': person['name'] if person['name'] != "" else person["username"], 
         'Posts': person['post_count'], 
         'Link': 'http://www.chiefdelphi.com/u/' + person['username']} for person in requests.get(cdThread).json()['details']['participants']]

gen.listOfDictToCSV('Girls Thread Posters', data, ['Person', 'Posts', 'Link'])