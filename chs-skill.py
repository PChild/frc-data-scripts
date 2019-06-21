import trueskill
import gen

dist = "2019chs"
tba = gen.setup()

team_ratings = {}
for team in tba.district_teams(dist):
    team_ratings[team.key] = trueskill.Rating()

for event in sorted(tba.district_events(dist), key=lambda k: k['week']):
    print('Processing', event.key)
    for match in sorted(tba.event_matches(event.key), key=lambda k: k['time']):

        # If the outcome ranks are a tie the order of winning vs losing team sets doesn't matter,
        # that's why the check for winner and loser are more loose than what is normally used.
        outcome = [0, 1] if match['winning_alliance'] not in ['red', 'blue'] else [0, 0]
        winner = 'red' if match['winning_alliance'] == 'red' else 'blue'
        loser = 'blue' if winner == 'red' else 'red'

        winners = []
        for team in match['alliances'][winner]['team_keys']:
            if team not in team_ratings:
                team_ratings[team] = trueskill.Rating()

            winners.append(team_ratings[team])

        losers = []
        for team in match['alliances'][loser]['team_keys']:
            if team not in team_ratings:
                team_ratings[team] = trueskill.Rating()

            losers.append(team_ratings[team])

        ratings_obj = [tuple(winners), tuple(losers)]

        ratings_obj = trueskill.rate(ratings_obj, ranks=outcome)

        for idx, team in enumerate(match['alliances'][winner]['team_keys']):
            team_ratings[team] = ratings_obj[0][idx]

        for idx, team in enumerate(match['alliances'][loser]['team_keys']):
            team_ratings[team] = ratings_obj[1][idx]

ratings_list = []
for team in team_ratings:
    ratings_list.append({'team': team, 'rating': trueskill.expose(team_ratings[team])})

ratings_list = sorted(ratings_list, key=lambda k: k['rating'], reverse=True)
gen.listOfDictToCSV(dist + ' TrueSkill Ratings', ratings_list, ['team', 'rating'])
