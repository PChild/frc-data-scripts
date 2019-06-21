import gen

tba = gen.setup()

dist = 'chs'

for year in range(2016, 2020):
    print('On year', year)

    distKey = str(year) + dist

    distData = []
    for team in tba.district_rankings(distKey):
        teamObj = {'team': team['team_key'][3:],
                   'prePts': 0,
                   'postPts': team['point_total'],
                   'preRank': 0,
                   'postRank': team['rank']}

        if len(team['event_points']) < 3:
            teamObj['prePts'] = teamObj['postPts']
        else:
            teamObj['prePts'] = team['event_points'][0]['total'] + team['event_points'][1]['total']

        distData.append(teamObj)

    preRanks = [team['team'] for team in sorted(distData, key=lambda k: k['prePts'], reverse=True)]

    for team in distData:
        team['preRank'] = preRanks.index(team['team']) + 1

    gen.listOfDictToCSV(distKey + ' DCMP Effect', distData, ['team', 'preRank', 'prePts', 'postRank', 'postPts'])
