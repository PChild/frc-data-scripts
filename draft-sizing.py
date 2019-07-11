import math

num_players = 14
num_teams = 12

def get_tier_size(players, teams):
    needed = players * 3

    tiers = []

    base_size = math.ceil(needed / teams)
    remaining = needed
    while remaining > base_size