import tbapy

tba = tbapy.TBA('DJRE7IGB1IBTCtvpZfFnn7aZfBWoY9bTIZfQFY7CVBZ8tWeNRX6x0XdISQ63skHv')
f = open("mdoxo2018.csv", 'w')

eventKey = '2018mdoxo'
teamList = tba.event_teams(eventKey, False, True)
winRars = []

for team in teamList:
    awards = tba.team_awards(team)
    
    for award in awards:
        event = award['event_key']
        if award['name'] == "District Event Winner" and event != eventKey:
            winRars.append({'team': team, 'event': event})
            break
        
allTeams = len(teamList)
yesWins = len(winRars)
noWins = allTeams - yesWins

#Extra Sharp Prediction: The winning alliance will feature two first-time district event winners.

nny = (noWins / allTeams) * ((noWins - 1) / (allTeams - 1)) * ((yesWins) / (allTeams - 2)) 
nyn = (noWins / allTeams) * ((yesWins) / (allTeams - 1)) * ((noWins - 1) / (allTeams - 2))
ynn = (yesWins / allTeams) * ((noWins) / (allTeams - 1) * (noWins - 1) / (allTeams - 2))

correctProb = nny + nyn + ynn