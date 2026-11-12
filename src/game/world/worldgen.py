import random
from dataclasses import dataclass, field

from ..creatures import monsters
from ..constants import FLOOR, HALL_GUARDS, ITEMS, LOOT_PER_FLOOR, TOTAL_FLOORS
from ..creatures.entity import Entity
from .floor import Floor
from .layouts import START_ROOM, TOP_FLOOR

Pos = tuple[int, int]


@dataclass
class FloorState:
    """Everything about a floor that must survive while the player is elsewhere."""
    floor: Floor
    monsters: list[Entity]
    explored: set[Pos]
    items: dict[Pos, list[str]] = field(default_factory=dict)


def generate_floor(rng: random.Random, floor_no: int) -> FloorState:
    if floor_no == TOTAL_FLOORS:
        floor = Floor.from_template(TOP_FLOOR, with_back=floor_no > 1)
        spawn = {"g": lambda x, y: monsters.spawn(rng.choice(HALL_GUARDS), x, y), "F": monsters.spawn_boss}
        return FloorState(floor, [spawn[kind](x, y) for x, y, kind in floor.fixed_spawns], set())
    floor = Floor.generate(rng, with_next=True, with_back=floor_no > 1, first_room=START_ROOM if floor_no == 1 else None)
    count = min(len(floor.rooms) - 1, 2 + floor_no)
    rooms = rng.sample(floor.rooms[1:], count)
    mons = [monsters.spawn(monsters.pick_kind(rng, floor_no), *room.center) for room in rooms]
    return FloorState(floor, mons, set(), scatter_items(rng, floor, floor_no, {(m.x, m.y) for m in mons}))


def scatter_items(rng: random.Random, floor: Floor, floor_no: int, taken: set[Pos]) -> dict[Pos, list[str]]:
    kinds = [name for name, item in ITEMS.items() if item.get("min_floor", 99) <= floor_no]
    weights = [ITEMS[name]["frequency"] for name in kinds]
    placed: dict[Pos, list[str]] = {}
    for _ in range(LOOT_PER_FLOOR):
        name = rng.choices(kinds, weights=weights)[0]
        for _ in range(30):
            room = rng.choice(floor.rooms)
            x, y = rng.randint(room.x, room.x + room.w - 1), rng.randint(room.y, room.y + room.h - 1)
            if floor.tiles[y][x] == FLOOR and (x, y) not in taken and (x, y) not in placed and (x, y) != floor.start:
                placed[(x, y)] = [name]
                break
    return placed
