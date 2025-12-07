"""27-point point-buy system for ability score generation."""

import random

_COST_TABLE = {8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 9}

# Returning the point-buy cost of a single ability score
def score_cost(score):
    if score not in _COST_TABLE:
        raise ValueError(f"Score must be between 8 and 15, got {score!r}")
    return _COST_TABLE[score]

# If given a dict of ability scores, return total point-buy cost
def total_cost(scores):
    return sum(score_cost(value) for value in scores.values())

# Checking if the given scores are in a valid range and total cost
def is_valid_point_buy(scores, total_points=27):
    try:
        cost = total_cost(scores)
    except ValueError:
        return False
    return cost == total_points

# Generating random valid point-buy scores
def random_point_buy(
    ability_names,
    total_points=27,
    rng=None,
    max_attempts=100000
    ):
    if rng is None:
        rng = random.Random()
    ability_names = list(ability_names)

    for _ in range(max_attempts):
        scores = {name: rng.randint(8, 15) for name in ability_names}
        if is_valid_point_buy(scores, total_points=total_points):
            return scores

    raise RuntimeError("Failed to generate a valid point-buy score")
