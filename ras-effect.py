from tqdm import tqdm
import tbapy
import json
import os

if __name__ == '__main__':
    tba = tbapy.TBA(os.getenv('TBA_KEY'))
    year_data = {}

    for year in tqdm(range(1992, 2020)):
        s_year = str(year)
        s1_year = str(year - 1)
        year_data[s_year] = {'teams': tba.teams(year=year, keys=True), 'gains': [], 'losses': []}

        if s1_year in year_data:
            year_data[s_year]['gains'] = [team for team in year_data[s_year]['teams']
                                          if team not in year_data[s1_year]['teams']]
            year_data[s_year]['losses'] = [team for team in year_data[s1_year]['teams']
                                        if team not in year_data[s_year]['teams']]
        else:
            year_data[s_year]['gains'] = year_data[s_year]['teams']

        with open('team_data_' + s_year + '.json', 'w') as fp:
            json.dump(year_data[s_year], fp)
