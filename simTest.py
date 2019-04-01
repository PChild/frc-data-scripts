import gen
import pandas
import eventTypes
from hallOfFame import hallOfFame
from rookieValues import rookieValues

tba = gen.setup()
district = 'fim'
runYear = 2019

probScale = 2500 #mCa

allDistTeams = pandas.read_csv(str(runYear) + ' District Teams.csv', header=None)[0].tolist()
mCA = pandas.read_csv('2018mCA.csv', index_col='Team')
mCA['Won CA'] = False
mCA['Event'] = ''
mCA['Win Prob'] = 0

for year in hallOfFame:
    for team in hallOfFame[year]:
        mCA.loc[team, 'Won CA'] = True
        mCA.loc[team, 'Event'] = 'HoF'

def predictCAWinner(event):
    probPivot = -10000
    totalProb = 1000
    
    isDistrict = False
    distInfo = tba.event(event)['district']
    
    if distInfo is not None:
        isDistrict = True
        eventDist = distInfo['key']
        distTeams = [int(team[3:]) for team in tba.district_teams(eventDist, False, True)]
        
    teams = [int(team[3:]) for team in tba.event_teams(event, False, True)]
    
    eventTeams = mCA.loc[teams]
    eventTeams['Win %'] = 0
    
    while totalProb > 1:
        if totalProb > 1.5:
            probPivot += 200
        else:
            probPivot += 10
        
        totalProb = 0
        
        for team in teams:
            lateRegister = team not in eventTeams.index
            
            if not lateRegister:
                invalidRegTeam = isDistrict and team not in distTeams
                invalidDistTeam = not isDistrict and team in allDistTeams
                alreadyWon = mCA.loc[team, 'Won CA']
                rookieTeam = team >= rookieValues[year]
                
                teamProb = 0
                
                if not alreadyWon and not rookieTeam and not invalidRegTeam and not invalidDistTeam:
                    teamProb = (1 / (1 + 10 ** ((probPivot - eventTeams.loc[team, 'milliCA Rating']) / probScale)))
                    
                totalProb += teamProb
                eventTeams.loc[team, 'Win %'] = teamProb
    eventTeams['Win %'] = eventTeams['Win %'] / totalProb
    return eventTeams.sort_values('Win %', ascending=False)


def predictDistrict(dist):
    rawEvents = tba.district_events(str(runYear) + dist)
    rawEvents = sorted(rawEvents, key=lambda k: k['start_date'])
    events = [event['key'] for event in rawEvents if event['event_type'] == eventTypes.DISTRICT]
    for event in events:
        eventCA = predictCAWinner(event)
        for val in range(0,3):
            caWinner = eventCA.index[val]
            winProb = eventCA.iloc[val]['Win %']
            
            if val == 0:
                mCA.loc[caWinner, 'Won CA'] = True
                mCA.loc[caWinner, 'Event'] = event
                mCA.loc[caWinner, 'Win Prob'] = winProb
            print(event, ' - ', caWinner, round(winProb * 100, 2), '%')
        print('\n')
        
def predictRegionals():
    regionalDf = pandas.read_csv('2019 Regionals.csv')
    
    for event in regionalDf['Code']:
        eventCA = predictCAWinner(event)
        caWinner = eventCA.index[0]
        winProb = eventCA.iloc[0]['Win %']
        mCA.loc[caWinner, 'Won CA'] = True
        mCA.loc[caWinner, 'Event'] = event
        mCA.loc[caWinner, 'Win Prob'] = winProb
        print(event, ' - ', caWinner, round(winProb * 100, 2), '%')
        
def main():
    print('memes')
    #predictRegionals()
        

if __name__ == '__main__':
    main()
