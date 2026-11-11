"""Numbers of the rules: speed, energy and the chance to hit."""

DEFAULT_SPEED = 100                           # 100 = one action per turn; lower is slower, higher faster
ACTION_COST = 100                             # energy an action costs; a turn grants `speed` energy
# Every attack, yours and the monsters', rolls against the target's DV:
#   chance to hit (%) = HIT_BASE + attack value - DV of the target, kept between HIT_MIN and HIT_MAX.
HIT_BASE, HIT_MIN, HIT_MAX = 50, 5, 95
BASE_DV = 10                                  # what you have before any gear
BASE_ATTACK = 40                              # your attack value before weapon bonuses
