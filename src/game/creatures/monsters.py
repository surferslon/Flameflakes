import random

from ..constants import BOSS, MONSTERS, SIGHT
from .entity import Entity
from ..world.floor import Floor


def spawn(kind: str, x: int, y: int) -> Entity:
    """A monster from the MONSTERS table, e.g. spawn("troll", 3, 4)."""
    stats = MONSTERS[kind]
    return Entity(x, y, stats["ch"], stats["color"], kind, stats["hp"], True,
                  damage=stats["damage"], speed=stats["speed"], attack=stats["attack"], dv=stats["dv"])


def pick_kind(rng: random.Random, floor_no: int) -> str:
    """A random monster that may appear on this floor; common ones come up more often."""
    kinds = [kind for kind, stats in MONSTERS.items()
             if stats["min_floor"] <= floor_no <= stats.get("max_floor", floor_no)]
    return rng.choices(kinds, weights=[MONSTERS[kind]["frequency"] for kind in kinds])[0]


def spawn_boss(x: int, y: int) -> Entity:
    return Entity(x, y, BOSS["ch"], BOSS["color"], BOSS["name"], BOSS["hp"], True, damage=BOSS["damage"],
                  speed=BOSS["speed"], attack=BOSS["attack"], dv=BOSS["dv"], boss=True)


def step_towards(mon: Entity, player: Entity, floor: Floor, blocked: set[tuple[int, int]]) -> None:
    sx = (player.x > mon.x) - (player.x < mon.x)
    sy = (player.y > mon.y) - (player.y < mon.y)
    for dx, dy in ((sx, sy), (sx, 0), (0, sy)):
        tx, ty = mon.x + dx, mon.y + dy
        if (dx or dy) and floor.is_walkable(tx, ty) and (tx, ty) not in blocked:
            mon.x, mon.y = tx, ty
            return


def is_adjacent(mon: Entity, player: Entity) -> bool:
    """Next to the player, diagonals included, so monsters can fight diagonally too."""
    return max(abs(mon.x - player.x), abs(mon.y - player.y)) == 1


def in_sight(mon: Entity, player: Entity) -> bool:
    return abs(mon.x - player.x) + abs(mon.y - player.y) < SIGHT
