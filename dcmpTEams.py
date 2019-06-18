import gen

tba = gen.setup()

dcmp = '2019chcmp'

gen.listToCSV(dcmp + ' Teams', sorted([int(team[3:]) for team in tba.event_teams(dcmp, keys = True)]))