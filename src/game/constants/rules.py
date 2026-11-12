"""Numbers of the rules: speed, energy and the chance to hit."""

DEFAULT_SPEED = 100  # 100 = one action per turn
ACTION_COST = 100
# Chance to hit (%) = HIT_BASE + attack value - DV of the target, kept between HIT_MIN and HIT_MAX.
HIT_BASE, HIT_MIN, HIT_MAX = 50, 5, 95
BASE_DV = 10
BASE_ATTACK = 40
