from bs4 import BeautifulSoup
import datetime
import requests
import gen

modUrl = 'https://www.chiefdelphi.com/forums/showgroups.php'

now = datetime.datetime.now()
timeStamp = now.strftime("%Y-%m-%d")

r = requests.get(modUrl)
soup = BeautifulSoup(r.content,"html.parser")

modData = []

gen.listOfDictToCSV('cdMods-' + timeStamp, modData, [])