import tbapy
from bs4 import BeautifulSoup
import requests
import time

tba = tbapy.TBA('DJRE7IGB1IBTCtvpZfFnn7aZfBWoY9bTIZfQFY7CVBZ8tWeNRX6x0XdISQ63skHv')
USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

DISTRICT = 'chs'
YEAR = '2018'

BASE_URL = 'http://www.google.com/search?q=frc+team+'
TYPES = ['facebook', 'twitter', 'youtube', 'github', 'instagram']
dataFields = ['profile', 'link']

districtTeams = tba.district_teams(YEAR + DISTRICT, True, False)
allTeamData = {}

def fetch_results(search_term, number_results, language_code):
    assert isinstance(search_term, str), 'Search term must be a string'
    assert isinstance(number_results, int), 'Number of results must be an integer'
    escaped_search_term = search_term.replace(' ', '+')

    google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_search_term, number_results, language_code)
    response = requests.get(google_url, headers=USER_AGENT)
    response.raise_for_status()

    return search_term, response.text

def parse_results(html, keyword):
    soup = BeautifulSoup(html, 'html.parser')
    found_results = ''
    result_block = soup.find_all('div', attrs={'class': 'g'})
    for result in result_block:
        link = result.find('a', href=True)
        if link:
            link = link['href']
            if link != '#':
                found_results = link
    return found_results

def scrape_google(search_term, number_results, language_code):
    try:
        keyword, html = fetch_results(search_term, number_results, language_code)
        results = parse_results(html, keyword)
        return results
    except AssertionError:
        raise Exception("Incorrect arguments parsed to function")
    except requests.HTTPError:
        raise Exception("You appear to have been blocked by Google")
    except requests.RequestException:
        raise Exception("Appears to be an issue with your connection")

for team in districtTeams:
    print("Processing team " + str(team['team_number']))
    teamData = []
    currentProfiles = tba.team_profiles(team['key'])
    neededProfiles = TYPES[:]
    
    for profile in currentProfiles:
        try:
            neededProfiles.remove(profile['type'][:-8])
        except:
            print("Couldn't remove " + profile['type'][:-8] + " from " + str(neededProfiles))

    for profile in neededProfiles:
        try:
            results = scrape_google(profile + " frc team " + str(team['team_number']), 1, "en")
            teamData.append({'profile': profile, 'link': results})
        except Exception as e:
            print(e)
        finally:
            time.sleep(1)
    allTeamData[team['key']] = teamData
    
f = open(DISTRICT + "MissingMedia.csv", 'w', encoding='utf-8')
for teamKey in allTeamData:
    f.write('https://www.thebluealliance.com/suggest/team/social_media?team_key=' + teamKey + ", ")
    for profile in allTeamData[teamKey]:
        for field in dataFields:
            f.write(profile[field] + ", ")
    f.write("\n")
f.close()