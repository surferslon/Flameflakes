import itertools
import random
import string
from dataclasses import dataclass

from ..constants import BACK, CHAOS_EXCLUDED, DOOR, FLOOR, H, NEXT, W, WALL


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
        self.start = start
        self.rooms = rooms if rooms is not None else []
        self.fixed_spawns = fixed_spawns

    @classmethod
    def generate(cls, rng: random.Random, with_next: bool = True, with_back: bool = True,
                 attempts: int = 40, first_room: list[str] | None = None) -> "Floor":
        while True:  # in the rare case that there is room for no more than one room, try again
            tiles = [[WALL] * W for _ in range(H)]
            rooms: list[Room] = []
            floor = cls(tiles, (0, 0), rooms)
            box = floor._place(rng, first_room) if first_room else None
            for _ in range(attempts):
                w, h = rng.randint(4, 10), rng.randint(3, 6)
                room = Room(rng.randint(1, W - w - 1), rng.randint(1, H - h - 1), w, h)
                if any(room.overlaps(other) for other in rooms) or (box and room.overlaps(box)):
                    continue
                if rooms:
                    path = (floor._leave_room(box, room.center) if box and len(rooms) == 1
                            else floor._route(rooms[-1].center, room.center, box))
                    if path is None:
                        continue
                    floor._carve(path)
                floor._carve_room(room)
                rooms.append(room)
            if len(rooms) >= 2:
                break
        if not box:
            floor.start = rooms[0].center
        if with_next:
            x, y = rooms[-1].x, rooms[-1].y
            tiles[y][x] = NEXT
        if with_back:
            x, y = floor.start
            tiles[y][x] = BACK
        return floor

    @classmethod
    def chaos(cls, rng: random.Random) -> "Floor":
        alphabet = [ch for ch in string.ascii_letters + string.digits + string.punctuation
                    if ch not in CHAOS_EXCLUDED]
        tiles = [[rng.choice(alphabet) for _ in range(W)] for _ in range(H)]
        return cls(tiles, (W // 2, H // 2))

    @classmethod
    def from_template(cls, template: list[str], with_back: bool = True) -> "Floor":
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
        return 0 <= x < W and 0 <= y < H and self.tiles[y][x] not in (WALL, DOOR)

    def stairs_at(self, x: int, y: int) -> str | None:
        return self.tiles[y][x] if self.tiles[y][x] in (NEXT, BACK) else None

    def find(self, tile: str) -> tuple[int, int]:
        return next((x, y) for y, row in enumerate(self.tiles) for x, t in enumerate(row) if t == tile)

    def rows(self) -> list[str]:
        return ["".join(row) for row in self.tiles]

    def _carve_room(self, room: Room) -> None:
        for y, x in itertools.product(range(room.y, room.y + room.h), range(room.x, room.x + room.w)):
            self.tiles[y][x] = FLOOR

    def _carve(self, path: list[tuple[int, int]]) -> None:
        for x, y in path:
            self.tiles[y][x] = FLOOR

    @staticmethod
    def _corridor(a: tuple[int, int], b: tuple[int, int], horizontal_first: bool) -> list[tuple[int, int]]:
        """An L-shaped path from a to b."""
        (ax, ay), (bx, by) = a, b
        if horizontal_first:
            return ([(x, ay) for x in range(min(ax, bx), max(ax, bx) + 1)]
                    + [(bx, y) for y in range(min(ay, by), max(ay, by) + 1)])
        return ([(ax, y) for y in range(min(ay, by), max(ay, by) + 1)]
                + [(x, by) for x in range(min(ax, bx), max(ax, bx) + 1)])

    def _route(self, a: tuple[int, int], b: tuple[int, int], box: Room | None) -> list[tuple[int, int]] | None:
        for horizontal_first in (True, False):
            path = self._corridor(a, b, horizontal_first)
            if not self._hits(path, box):
                return path
        return None

    @staticmethod
    def _hits(path: list[tuple[int, int]], box: Room | None) -> bool:
        return bool(box) and any(box.x <= x < box.x + box.w and box.y <= y < box.y + box.h for x, y in path)

    def _leave_room(self, box: Room, target: tuple[int, int]) -> list[tuple[int, int]]:
        tx, ty = target
        cx, cy = box.x + box.w // 2, box.y + box.h // 2
        if ty < box.y:
            gap, out, vertical = (cx, box.y), (cx, box.y - 1), True
        elif tx < box.x:
            gap, out, vertical = (box.x, cy), (box.x - 1, cy), False
        else:
            gap, out, vertical = (box.x + box.w - 1, cy), (box.x + box.w, cy), False
        return [gap] + self._corridor(out, target, horizontal_first=not vertical)

    def _place(self, rng: random.Random, template: list[str]) -> Room:
        h, w = len(template), len(template[0])
        left, top = rng.randint(2, W - w - 2), H - h  # on the bottom edge of the map: nothing behind its door
        for y, row in enumerate(template):
            for x, ch in enumerate(row):
                if ch == "@":
                    self.start = (left + x, top + y)
                    ch = FLOOR
                self.tiles[top + y][left + x] = ch
        self.rooms.append(Room(left + 1, top + 1, w - 2, h - 2))
        return Room(left, top, w, h)
