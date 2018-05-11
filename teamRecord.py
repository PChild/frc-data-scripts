import tbapy
import pandas as pd
from os import getenv

def removeFRC(s):
    return int(''.join(filter(str.isdigit, s)))
def getTeamData(team):
    opponents = {}

    officialWins = 0
    officialLoss = 0
    officialTies = 0
    
    totalWins = 0
    totalLoss = 0
    totalTies = 0
    
    offseasonWins = 0
    offseasonLoss = 0
    offseasonTies = 0
        
    for year in tba.team_years(team):
        print("Fetching ", str(team), " events in ", str(year))
        for event in tba.team_events(team, year, False):
           print("Processing ", str(team), " at ", event['short_name'])
           for match in tba.team_matches(team, event['key']):
               redRaw = match['alliances']['red']['team_keys']
               blueRaw = match['alliances']['blue']['team_keys']
                          
               redTeams = [removeFRC(s) for s in redRaw]
               blueTeams = [removeFRC(s) for s in blueRaw]
               
               myTeam = "red" if team in redTeams else "blue"
               winner = match['winning_alliance']
               
               officialEvent = event['event_type'] >= -1 and event['event_type'] < 10
               
               if officialEvent:
                   if myTeam == winner:
                       officialWins += 1
                       totalWins += 1
                   elif winner == "":
                       officialTies += 1
                       totalTies += 1
                   else:
                       officialLoss += 1
                       totalLoss += 1
               else:
                   if myTeam == winner:
                       totalWins += 1
                       offseasonWins += 1
                   elif winner == "":
                       totalTies += 1
                       offseasonTies += 1
                   else:
                       totalLoss += 1
                       offseasonLoss += 1
                   
               opposingAlliance = blueTeams if team in redTeams else redTeams
               
               for oppoTeam in opposingAlliance:
                   if oppoTeam not in opponents:
                       opponents[oppoTeam]= {
                               'Overall Wins': 0, 'Overall Ties': 0, 'Overall Losses': 0, 
                               'Official Wins': 0, 'Official Ties': 0, 'Official Losses': 0, 
                               'Offseason Wins': 0, 'Offseason Losses': 0, 'Offseason Ties': 0}
                   if officialEvent:
                       if myTeam == winner:
                           opponents[oppoTeam]['Official Wins'] += 1
                           opponents[oppoTeam]['Overall Wins'] += 1
                       elif winner == "":
                           opponents[oppoTeam]['Official Ties'] += 1
                           opponents[oppoTeam]['Overall Ties'] += 1
                       else:
                           opponents[oppoTeam]['Official Losses'] += 1
                           opponents[oppoTeam]['Overall Losses'] += 1
                   else:
                       if myTeam == winner:
                           opponents[oppoTeam]['Overall Wins'] += 1
                           opponents[oppoTeam]['Offseason Wins'] += 1
                       elif winner == "":
                           opponents[oppoTeam]['Overall Ties'] += 1
                           opponents[oppoTeam]['Offseason Ties'] += 1
                       else:
                           opponents[oppoTeam]['Overall Losses'] += 1
                           opponents[oppoTeam]['Offseason Losses'] += 1
    
    overall = {'Overall Wins': totalWins,'Overall Losses': totalLoss, 'Overall Ties': totalTies, 
                               'Official Wins': officialWins,'Official Losses': officialLoss, 'Official Ties': officialTies, 
                               'Offseason Wins': offseasonWins,'Offseason Losses': offseasonLoss, 'Offseason Ties': offseasonTies }
    
    overall = pd.DataFrame(overall, index=[team])
    overall.index.name = 'Team Number'
    data = pd.DataFrame(opponents).transpose()
    fileName = getenv('USERPROFILE') + "\\Desktop\\" + str(team) + " Record.xlsx"
    data.index.name = 'Team Number'
    writer = pd.ExcelWriter(fileName, engine='xlsxwriter')
    overall.to_excel(writer, sheet_name='Sheet1', startrow=1)
    data.to_excel(writer, sheet_name='Sheet1', startrow=4)
    writer.save()
    
    newTeam = input("\nTeam " + str(team) + " data file written to desktop. \nPress ENTER to exit, or \nEnter Team Number: ")
    
    if (newTeam == ""):
        print("Exiting")
    else:
        getTeamData(int(newTeam))

tba = tbapy.TBA('DJRE7IGB1IBTCtvpZfFnn7aZfBWoY9bTIZfQFY7CVBZ8tWeNRX6x0XdISQ63skHv')

print("FRC Team Record Finder by Team 401")
team = int(input("Enter Team Number: "))
getTeamData(team)    