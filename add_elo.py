# this is part of a much larger local db I have

from django.core.management.base import BaseCommand
from fwhr.whole_history_rating import Base
from core.models import Event, Team
from typing import Callable
from collections import defaultdict
from AutoScout.settings import SUPPORTED_YEARS, PER_YEAR_ELO_OFFSET
# SUPPORTED_YEARS is [2017, 2018]
# PER_YEAR_ELO_OFFSET is a constant, tunable, but currently equal to 75

num_weeks_per_year = {year: Event.objects.filter(year=year).values_list('week', flat=True).distinct().count()
                      for year in SUPPORTED_YEARS}


def get_timestep_for_event(event: Event) -> int:
    timestep = 0
    for year, weeks in sorted(num_weeks_per_year.items(), key=lambda t: t[0]):
        if event.year == year:
            return timestep + event.week * 7
        else:
            timestep += weeks * 7 + PER_YEAR_ELO_OFFSET

    raise ValueError('Should not hit this case')


def get_elos_for_teams(base, teams):
    elos = []
    for team in teams:
        try:
            ratings = base.ratings_for_player(str(team.id), current=True)
            elos.append(ratings[0])
        except IndexError:
            elos.append(0)

    return elos


def average_elo(base, teams):
    elos = get_elos_for_teams(base, teams)
    return sum(elos) / len(elos)


def weighted_avg(base, teams):
    elos = get_elos_for_teams(base, teams)
    elos.sort()
    return 0.4 * elos[-1] + 0.4 * elos[-2] + 0.2 * elos[0]

# utility class to compare methods. i cut out the code from a bunch of other methods.
# Command.handle3() is the best one i've gotten so far.
class LadderManager:
    def __init__(self):
        self.ladders = {}

    def add_ladder(self, ladder: Base, reduce: Callable):
        self.ladders[reduce] = ladder

    def print_all(self):
        ladder_ranks = defaultdict(lambda: list())
        for ladder in self.ladders.values():
            ranks = reversed(ladder.get_ordered_ratings(current=True))
            rank = 1
            for player, elo in ranks:
                if LadderManager.__is_number(player):  # this is an artifact of a previous attempt. ignore the if
                    ladder_ranks[rank].append((player, elo))
                    Team.objects.filter(id=int(player)).update(elo=elo)
                    rank += 1

        from pprint import pprint
        pprint(sorted(ladder_ranks.items())[:10])

    @staticmethod
    def __is_number(x):
        try:
            int(x)
            return True
        except ValueError:
            return False


class Command(BaseCommand):
    def handle(self, *args, **options):
        Team.objects.update(elo=0)
        self.handle3(Event.objects.order_by('start_date'))

    def handle3(self, events):
        mgr = LadderManager()
        mgr.add_ladder(Base('Average Elo'), average_elo)
        # mgr.add_ladder(Base('Weighted Avg'), weighted_avg)

        for event in events:
            time = get_timestep_for_event(event)
            print(time, event.key)
            matches = list(event.match_set.all())
            matches.sort(key=lambda m: (['qm', 'ef', 'qf', 'sf', 'f'].index(m.comp_level), m.match_number))

            for match in matches:
                winners = match.winners_played.all()
                losers = match.losers_played.all()

                if match.comp_level == 'qm':
                    for winner in winners:
                        for loser in losers:
                            for fn, ladder in mgr.ladders.items():
                                ladder.create_game(str(winner.id), str(loser.id), "B", time, 0)
                else:
                    if match.winner is not None:
                        winner = match.winner
                        loser = match.loser

                        pairs = [
                            (winner.captain, loser.captain),
                            (winner.captain, loser.first_pick),
                            (winner.first_pick, loser.captain),
                            (winner.first_pick, loser.first_pick),
                            (winner.second_pick, loser.second_pick),
                            (winner.second_pick, loser.third_pick),
                            (winner.third_pick, loser.second_pick),
                            (winner.third_pick, loser.third_pick)
                        ]

                        for fn, ladder in mgr.ladders.items():
                            for pair in pairs:
                                if pair[0] in match.played.all() and pair[1] in match.played.all():
                                    ladder.create_game(str(pair[0].id), str(pair[1].id), "B", time, 0)

                    else:
                        for r in match.red_played.all():
                            for b in match.blue_played.all():
                                for fn, ladder in mgr.ladders.items():
                                    ladder.create_game(str(r.id), str(b.id), "B", time, 0)
                                    ladder.create_game(str(r.id), str(b.id), "W", time, 0)

        for fn, ladder in mgr.ladders.items():
            # ladder.auto_iterate(time_limit=600, precision=10E-3)
            ladder.iterate(10)

        mgr.print_all()
