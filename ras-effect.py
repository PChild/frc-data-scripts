import tbapy
import os

year_data= {}

if __name__ == '__main__':
    tba = tbapy.TBA(os.getenv('TBA_KEY'))

    for year in range(1992, 2020):
        year_data[str(year)] = {'teams': [], 'gained': [], 'lost': []}

        if str(year - 1) in year_data:
            year_data[str(year)]['gaind']
        tba.teams(year=year, keys=True)
    print('hi')
