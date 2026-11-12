import random

from ..constants import FLOOR, NEXT, W, H
from ..creatures.entity import Entity
from .floor import Floor
from .fov import visible_tiles
from .worldgen import FloorState, Pos, generate_floor


class World:
    """All the floors and the one the player is on. Floors are built on the first visit and stay as they were."""

    def __init__(self, rng: random.Random) -> None:
        self.rng = rng
        self.visited: dict[int, FloorState] = {}
        self.floor_no = 0
        self.level_id = 0
        self.chaos = False
        self.visible: set[Pos] = set()

    def enter(self, number: int, from_below: bool, player: Entity) -> None:
        if self.floor_no:
            self.visited[self.floor_no] = FloorState(self.floor, self.monsters, self.explored, self.items)
        self.floor_no = number
        saved = self.visited.get(number) or generate_floor(self.rng, number)
        self.floor, self.monsters, self.explored, self.items = saved.floor, saved.monsters, saved.explored, saved.items
        player.x, player.y = self.floor.start if from_below else self.floor.find(NEXT)
        self.level_id += 1
        self.reveal(player)

    def enter_chaos(self, player: Entity) -> None:
        self.chaos = True
        self.floor = Floor.chaos(self.rng)
        self.monsters, self.items = [], {}
        player.x, player.y = self.floor.start
        self.level_id += 1
        self.reveal(player)

    def reveal(self, player: Entity) -> None:
        if self.chaos:
            self.visible = {(x, y) for x in range(W) for y in range(H)}
            self.explored = set(self.visible)
            return
        self.visible = visible_tiles(self.floor, player.x, player.y)
        self.explored |= self.visible

    def monster_at(self, x: int, y: int) -> Entity | None:
        return next((m for m in self.monsters if m.x == x and m.y == y), None)

    def tile(self, x: int, y: int) -> str:
        return self.floor.tiles[y][x]

    def can_drop_at(self, x: int, y: int) -> bool:
        return self.tile(x, y) == FLOOR
