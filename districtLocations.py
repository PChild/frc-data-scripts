import gen

tba = gen.setup()

distTeams = tba.district_teams('2018chs')

teamList = []

for team in distTeams:
    if team['state_prov'] == 'Virginia':
        teamList.append({'Team': team['key'][3:], 'Sponsors': team['name'].replace(',', ''), 'Location': team['city'] + ' ' + team['state_prov'] + ' ' + str(team['postal_code']) })
        
gen.listOfDictToCSV('Virginia Team Locations', teamList, ['Team', 'Location', 'Sponsors'])