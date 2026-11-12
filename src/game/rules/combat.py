import random

from . import dice
from ..constants import HIT_BASE, HIT_MAX, HIT_MIN
from ..creatures.entity import Entity
from ..items.gear import Gear


def hit_chance(attack: int, dv: int) -> int:
    """Percent chance that an attack with this attack value hits a target with this DV."""
    return max(HIT_MIN, min(HIT_MAX, HIT_BASE + attack - dv))


def _hits(rng: random.Random, attack: int, dv: int) -> bool:
    return rng.randint(1, 100) <= hit_chance(attack, dv)


def player_attacks(rng: random.Random, gear: Gear, target: Entity) -> list[str]:
    if not _hits(rng, gear.attack, target.dv):
        return [f"You miss the {target.name}."]
    amount = max(0, dice.roll(rng, gear.damage))  # a negative roll (3d13-9) is just a hit that does nothing
    target.hp -= amount
    lines = [f"You hit the {target.name} for {amount}."]
    if target.hp <= 0:
        lines.append(f"The {target.name} dies.")
    return lines


def monster_attacks(rng: random.Random, mon: Entity, gear: Gear, player: Entity) -> str:
    if not _hits(rng, mon.attack, gear.dv):
        return f"The {mon.name} misses you."
    amount = max(0, dice.roll(rng, mon.damage) - gear.pv)
    player.hp -= amount
    return f"The {mon.name} hits you for {amount}."
