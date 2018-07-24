from multiprocessing import Pool
from functools import partial
import gen

year = 2018
yearRange = 5
teamData = []

years = range(year - yearRange + 1, year + 1)
tba = gen.setup()

def teamsHelper(year, page):
    return tba.teams(page, year, False, True)

def teamEvents(year, team):
    events = sorted(tba.team_events(team, year, True, False), key = lambda k: k['start_date'])
    eventKeys = [event['key'] for event in events]
    return {'team': team, 'year': year, 'events': eventKeys}

def main(year):
    global teamData
    teamKeys = []
    tmpData = []
    pool = Pool()
    
    mapData = pool.map(partial(teamsHelper, year), range(0, 16))

    for page in mapData:
        teamKeys+= page
            
    for year in years:
        tmpData += pool.map(partial(teamEvents, year), teamKeys)    
    teamData = tmpData
    
    pool.close()
    pool.join()
             
if __name__ == "__main__":
    main(year)