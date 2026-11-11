"""Dice notation {x}d{y}+{z}: roll {x} dice with {y} faces each, add them up and finally add {z}.

{z} can be positive or negative; without it, it is 0.
    1d20     one 20-sided die: 1 to 20
    2d6      two 6-sided dice: 2 to 12
    4d4+3    four 4-sided dice plus 3: 7 to 19
    3d13-9   three 13-sided dice minus 9: -6 to 30
"""
import random
import re

_DICE = re.compile(r"(\d+)d(\d+)([+-]\d+)?")


def parse(spec: str) -> tuple[int, int, int]:
    """"4d4+3" -> (4, 4, 3): how many dice, how many sides each, what is added at the end."""
    match = _DICE.fullmatch(spec)
    if not match or int(match[1]) < 1 or int(match[2]) < 1:
        raise ValueError(f"not dice notation: {spec!r} (expected something like '2d6' or '4d4+3')")
    return int(match[1]), int(match[2]), int(match[3] or 0)


def bounds(spec: str) -> tuple[int, int]:
    """The lowest and highest result of a roll."""
    count, sides, bonus = parse(spec)
    return count + bonus, count * sides + bonus


def roll(rng: random.Random, spec: str) -> int:
    count, sides, bonus = parse(spec)
    return sum(rng.randint(1, sides) for _ in range(count)) + bonus
