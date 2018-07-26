import gen
import slff
import pandas as pd

tba = gen.setup()

teamSponsors = pd.read_csv('Team Sponsors.csv')
year = 2018

oprData = []
for team in teamSponsors['Team']:
    oprData.append(slff.getPerformanceData(team, year)['Avg OPR'])
    
teamSponsors = teamSponsors.assign(OPR=oprData)
teamSponsors.to_csv('Sponsor OPRs.csv')