import gen
import eventTypes
import awardTypes
from tqdm import tqdm

bannerTypes = [awardTypes.WINNER, awardTypes.CHAIRMANS, awardTypes.WOODIE_FLOWERS]

tba = gen.setup()
year = 2019

best = {'team': '', 'bannerCount': 0}
for team in tqdm(tba.teams(year=year, keys=True)):
    events = tba.team_events(team, year)
    madeChamps = False
    for event in events:
        if event.event_type is eventTypes.CMP_DIVISION:
            madeChamps = True
    
    bannerCount = 0
    if not madeChamps:
        for event in events:
            for award in tba.team_awards(team, year, event.key):
                if award.award_type in bannerTypes:
                   bannerCount += 1 
        
        if bannerCount > best['bannerCount']:
            best['team'] = team
            best['bannerCount'] = bannerCount
print(best)