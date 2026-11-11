import itertools
import random
import string
from dataclasses import dataclass

from ..constants import BACK, CHAOS_EXCLUDED, FLOOR, H, NEXT, W, WALL


@dataclass(frozen=True)
class Room:
    x: int
    y: int
    w: int
    h: int

    @property
    def center(self) -> tuple[int, int]:
        return self.x + self.w // 2, self.y + self.h // 2

    def overlaps(self, other: "Room") -> bool:
        return (self.x < other.x + other.w + 1 and self.x + self.w + 1 > other.x
                and self.y < other.y + other.h + 1 and self.y + self.h + 1 > other.y)


class Floor:
    def __init__(self, tiles: list[list[str]], start: tuple[int, int],
                 rooms: list[Room] | None = None,
                 fixed_spawns: list[tuple[int, int, str]] | None = None):
        self.tiles = tiles
        self.start = start                # where the player arrives from below
        self.rooms = rooms if rooms is not None else []  # only for generated floors
        self.fixed_spawns = fixed_spawns  # (x, y, "g" | "F") for hand-made floors, else None

    @classmethod
    def generate(cls, rng: random.Random, with_next: bool = True, with_back: bool = True,
                 attempts: int = 40) -> "Floor":
        tiles = [[WALL] * W for _ in range(H)]
        rooms: list[Room] = []
        floor = cls(tiles, (0, 0), rooms)
        for _ in range(attempts):
            w, h = rng.randint(4, 10), rng.randint(3, 6)
            room = Room(rng.randint(1, W - w - 1), rng.randint(1, H - h - 1), w, h)
            if any(room.overlaps(other) for other in rooms):
                continue
            floor._carve_room(room)
            if rooms:
                floor._carve_corridor(rooms[-1].center, room.center)
            rooms.append(room)
        floor.start = rooms[0].center
        if with_next:
            x, y = rooms[-1].x, rooms[-1].y
            tiles[y][x] = NEXT  # entrance to the next floor
        if with_back:
            x, y = floor.start
            tiles[y][x] = BACK
        return floor

    @classmethod
    def chaos(cls, rng: random.Random) -> "Floor":
        """A level of pure chaos: every tile is a random letter, digit or symbol, all walkable."""
        alphabet = [ch for ch in string.ascii_letters + string.digits + string.punctuation
                    if ch not in CHAOS_EXCLUDED]
        tiles = [[rng.choice(alphabet) for _ in range(W)] for _ in range(H)]
        return cls(tiles, (W // 2, H // 2))

    @classmethod
    def from_template(cls, template: list[str], with_back: bool = True) -> "Floor":
        """Build a hand-made floor from ASCII art (see layouts.py)."""
        tiles: list[list[str]] = []
        spawns: list[tuple[int, int, str]] = []
        start = (0, 0)
        for y, row in enumerate(template):
            assert len(row) == W and len(template) == H, "template must be W x H"
            line = []
            for x, ch in enumerate(row):
                if ch in ("g", "F"):
                    spawns.append((x, y, ch))
                    ch = FLOOR
                elif ch == BACK:
                    start = (x, y)
                    ch = BACK if with_back else FLOOR
                line.append(ch)
            tiles.append(line)
        return cls(tiles, start, fixed_spawns=spawns)

    width = W
    height = H

    def is_walkable(self, x: int, y: int) -> bool:
        return 0 <= x < W and 0 <= y < H and self.tiles[y][x] != WALL

    def stairs_at(self, x: int, y: int) -> str | None:
        return self.tiles[y][x] if self.tiles[y][x] in (NEXT, BACK) else None

    def find(self, tile: str) -> tuple[int, int]:
        return next((x, y) for y, row in enumerate(self.tiles) for x, t in enumerate(row) if t == tile)

    def rows(self) -> list[str]:
        return ["".join(row) for row in self.tiles]

    def _carve_room(self, room: Room) -> None:
        for y, x in itertools.product(range(room.y, room.y + room.h), range(room.x, room.x + room.w)):
            self.tiles[y][x] = FLOOR

    def _carve_corridor(self, a: tuple[int, int], b: tuple[int, int]) -> None:
        (ax, ay), (bx, by) = a, b
        for x in range(min(ax, bx), max(ax, bx) + 1):
            self.tiles[ay][x] = FLOOR
        for y in range(min(ay, by), max(ay, by) + 1):
            self.tiles[y][bx] = FLOOR
