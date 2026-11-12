import random
from collections.abc import Callable

from ..rules import combat
from ..creatures import monsters
from ..constants import ACTION_COST, BACK, GRAIL, GRAIL_NAME, NEXT
from ..creatures.entity import Entity
from ..items.inventory import Inventory, pile_text
from ..world.world import World


class Turns:
    def __init__(self, rng: random.Random, player: Entity, world: World, inventory: Inventory,
                 log: Callable[[str], None]) -> None:
        self.rng, self.player, self.world, self.inventory, self.log = rng, player, world, inventory, log

    def player_acts(self, dx: int, dy: int) -> bool:
        p, world = self.player, self.world
        if target := world.monster_at(p.x + dx, p.y + dy):
            self._strike(target)
            return True
        if not (dx or dy):
            return True
        if not world.floor.is_walkable(p.x + dx, p.y + dy):
            return False
        p.x, p.y = p.x + dx, p.y + dy
        world.reveal(p)
        self._notice_what_lies_here()
        return True

    def monsters_act(self) -> bool:
        p = self.player
        for mon in self.world.monsters:
            mon.energy += mon.speed * ACTION_COST / p.speed
            while mon.energy >= ACTION_COST:
                mon.energy -= ACTION_COST
                if self._monster_acts(mon):
                    return True
        return False

    def _strike(self, target: Entity) -> None:
        for line in combat.player_attacks(self.rng, self.inventory.gear, target):
            self.log(line)
        if target.hp <= 0:
            self.world.monsters.remove(target)
            if target.boss:
                self.log("The way to the Grail is open.")

    def _notice_what_lies_here(self) -> None:
        p, world = self.player, self.world
        if world.tile(p.x, p.y) == GRAIL:
            self.log(f"The {GRAIL_NAME} lies here. Press F to take it.")
        hints = {NEXT: "Stairs up. Press F to climb.", BACK: "Stairs down. Press F to go back."}
        if stairs := world.floor.stairs_at(p.x, p.y):
            self.log(hints[stairs])
        if pile := world.items.get((p.x, p.y)):
            self.log(pile_text(pile))

    def _monster_acts(self, mon: Entity) -> bool:
        p = self.player
        if monsters.is_adjacent(mon, p):
            self.log(combat.monster_attacks(self.rng, mon, self.inventory.gear, p))
            return p.hp <= 0
        if monsters.in_sight(mon, p):
            blocked = {(m.x, m.y) for m in self.world.monsters} | {(p.x, p.y)}
            monsters.step_towards(mon, p, self.world.floor, blocked)
        return False
