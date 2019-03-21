from bs4 import BeautifulSoup as bs
import requests

url = 'https://www.firstinspires.org/team-event-search/event?id=37526'

raw = requests.get(url)
soup = bs(raw.content, "lxml")