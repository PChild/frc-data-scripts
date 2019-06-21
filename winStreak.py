import gen
import awardTypes
from tqdm import tqdm

tba = gen.setup()

dist = 'chs'
currYear = 2019

distKey = str(currYear) + dist

teamStreaks = []
for team in tqdm(tba.district_teams(distKey)):
    teamData = {'team': team['team_number'],
                'currStart': 0,
                'currEnd': 0,
                'longest': 0,
                'current': 0,
                'longStart': 0,
                'longEnd': 0}

    for year in tba.team_years(team['key']):
        eventWinner = False
        for award in tba.team_awards(team['key'], year):
            if award['award_type'] == awardTypes.WINNER:
                eventWinner = True
        if eventWinner:
            if teamData['current'] == 0:
                teamData['currStart'] = year

            teamData['current'] += 1
            teamData['currEnd'] = year

            if teamData['current'] > teamData['longest']:
                teamData['longest'] = teamData['current']
                teamData['longStart'] = teamData['currStart']
                teamData['longEnd'] = teamData['currEnd']
        else:
            teamData['current'] = 0
            teamData['currStart'] = year
            teamData['currEnd'] = year
    teamStreaks.append(teamData)

gen.listOfDictToCSV(distKey.upper() + ' Streaks', teamStreaks,
                    ['team', 'currStart', 'currEnd', 'current', 'longStart', 'longEnd', 'longest'])


