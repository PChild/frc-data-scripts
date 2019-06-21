import tbapy
import os

hof_teams = ['frc16', 'frc23', 'frc27', 'frc51', 'frc67', 'frc103', 'frc111', 'frc120', 'frc175', 'frc236', 'frc254',
             'frc341', 'frc359', 'frc365', 'frc597', 'frc842', 'frc987', 'frc1114', 'frc1538', 'frc2614', 'frc3132',
             'frc2834', 'frc1311', 'frc1816', 'frc1902']

tba = tbapy.TBA(os.getenv("TBA_KEY"))

hof_matches = {}
for team in hof_teams:
    print('on team', team)
    for year in tba.team_years(team):
        for match in tba.team_matches(team, year=year):
            red_bots = match['alliances']['red']['team_keys']
            blue_bots = match['alliances']['blue']['team_keys']
            alliance = red_bots if team in red_bots else blue_bots

            all_hof = True
            for bot in alliance:
                all_hof = all_hof and bot in hof_teams

            if all_hof:
                if match['key'] not in hof_matches:
                    hof_matches[match['key']] = alliance

print('\n\nHOF ALLIANCE MATCHES:')
for key in hof_matches:
    print(key, '-', hof_matches[key])
