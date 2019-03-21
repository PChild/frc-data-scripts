import gen
from tqdm import tqdm
import pandas as pd

tba = gen.setup()
baseTeams = {}
for year in range(1992, 2020):
        print('Fetching teams for', year)
        for page in tqdm(range(0,30)):
                newTeams = tba.teams(page,  year)
                if newTeams == []:
                    break;
                else:
                    for team in newTeams:
                        key = team['key']
                        if key in baseTeams:
                            break
                        else:
                            baseTeams[key] = team
                            
testDF = pd.DataFrame(baseTeams)