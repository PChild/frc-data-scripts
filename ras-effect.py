from tqdm import tqdm
import awardTypes
import tbapy
import json
import os

tba = tbapy.TBA(os.getenv('TBA_KEY'))


def get_year_data():
    teams_data = {}

    for year in tqdm(range(1992, 2020)):
        s_year = str(year)
        s1_year = str(year - 1)
        teams_data[s_year] = {'teams': tba.teams(year=year, keys=True), 'gains': [], 'losses': []}

        if s1_year in teams_data:
            teams_data[s_year]['gains'] = [team for team in teams_data[s_year]['teams']
                                          if team not in teams_data[s1_year]['teams']]
            teams_data[s_year]['losses'] = [team for team in teams_data[s1_year]['teams']
                                           if team not in teams_data[s_year]['teams']]
        else:
            teams_data[s_year]['gains'] = teams_data[s_year]['teams']

        teams_data[s_year] = get_rookie_winners(year, teams_data[s_year])

        with open('team_data_' + s_year + '.json', 'w') as fp:
            json.dump(teams_data[s_year], fp)


def get_rookie_winners(year, year_data):
    year_data['ras'] = []
    year_data['ri'] = []
    year_data['seed'] = []

    for team in year_data['gains']:
        team_awards = [award.award_type for award in tba.team_awards(team, year)]

        if awardTypes.ROOKIE_ALL_STAR in team_awards:
            year_data['ras'].append(team)
        if awardTypes.ROOKIE_INSPIRATION in team_awards:
            year_data['ri'].append(team)
        if awardTypes.HIGHEST_ROOKIE_SEED in team_awards:
            year_data['seed'].append(team)

    return year_data


if __name__ == '__main__':
    for year in tqdm(range(1992, 2020)):
        year_info = json.load(open('team_data_' + str(year) + '.json'))

        for team in
        for new_year in range(year, 2020):
