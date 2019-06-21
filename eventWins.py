import gen
import awardTypes
from tqdm import tqdm

tba = gen.setup()

year = 2019
dist = 'chs'

distKey = str(year) + dist 

awards = []

for team in tqdm(tba.district_teams(distKey, False, True)):
    for award in tba.team_awards(team):
        if award['award_type'] is awardTypes.WINNER: 
            awards.append({'Team': team[3:],
                           'Year': award['event_key'][:4],
                           'Event': award['event_key'][4:],
                           'Name': award['name']})

gen.listOfDictToCSV(distKey + " Event Wins", awards, ['Team', 'Year', 'Event', 'Name'])