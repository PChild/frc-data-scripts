import math


def get_tier_sizes(num_players, num_teams, num_picks=3):
    tiers = math.ceil(num_players / math.floor(num_teams / num_picks))
    current_size = math.floor(num_players / tiers)

    tier_sizes = []

    while num_players > current_size:
        tier_sizes.append(current_size)
        num_players -= current_size
        tiers -= 1
        current_size = math.floor(num_players / tiers)

    tier_sizes.append(num_players)

    return tier_sizes


if __name__ == '__main__':
    players = 47
    teams = 68

    print(get_tier_sizes(players, teams))
