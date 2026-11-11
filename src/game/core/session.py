import random

from ..constants import (BACK, DEFAULT_SPEED, DIRECTIONS, ENDING_HINT, ENDING_PAGES, GRAIL, GRAIL_NAME, HEAL_ON_CLIMB,
                        INTRO_HINT, INTRO_PAGES, NEXT, PLAYER_HP, DEATH_MESSAGE, THE_END, TOTAL_FLOORS, FLOOR)
from ..creatures.entity import Entity
from ..items.inventory import Inventory
from ..narrative.message_log import MessageLog
from ..narrative.story import Story
from ..world.world import World
from .turns import Turns
from .view import ClientView


class Game:
    def __init__(self, seed: int | None = None, intro: bool = True):
        self.rng = random.Random(seed)
        self.log_lines = MessageLog()
        self.story = Story(INTRO_PAGES, INTRO_HINT) if intro else Story()
        self.turn = 0
        self.dead = False
        self.won = False
        self.player = Entity(0, 0, "@", "#fff", "you", PLAYER_HP)
        self.inventory = Inventory()
        self.world = World(self.rng)
        self.turns = Turns(self.rng, self.player, self.world, self.inventory, self.log)
        self.view = ClientView(self)
        self._refresh_stats()
        self.world.enter(1, from_below=True, player=self.player)

    @property
    def reading(self) -> bool:
        return self.story.reading

    @property
    def finished(self) -> bool:
        return self.dead or self.won

    def log(self, msg: str) -> None:
        self.log_lines.add(self.turn, msg)

    def state(self) -> dict:
        return self.view.state()

    def handle(self, action: str, arg: int | str | None = None) -> None:
        if self.story.reading:  # nothing moves until the story page has been read
            if action == "confirm" and self.story.confirm():
                self._story_over()
            return
        if self.finished:
            return
        pos = (self.player.x, self.player.y)
        if action == "interact":
            self._interact()
        elif action == "equip":
            self._handled(*self.inventory.equip(arg))
        elif action == "unequip":
            self._handled(*self.inventory.unequip(arg))
        elif action == "drop":
            if self.world.can_drop_at(*pos):
                self._handled(*self.inventory.drop(self.world.items, pos, arg))
            else:
                self.log("You cannot drop it here.")
        elif action in DIRECTIONS and self.turns.player_acts(*DIRECTIONS[action]):
            self._end_turn()

    def _refresh_stats(self) -> None:
        self.player.speed = DEFAULT_SPEED + self.inventory.gear.speed_bonus

    def _end_turn(self) -> None:
        if self.turns.monsters_act():
            self.dead = True
            self.log(DEATH_MESSAGE)
        self.turn += 1

    def _handled(self, done: bool, messages: list[str]) -> None:
        """Log what the inventory says. If something happened it took a turn."""
        for message in messages:
            self.log(message)
        if done:
            self._refresh_stats()
            self._end_turn()

    def _interact(self) -> None:
        """F: use the stairs, take the Grail, or pick up what lies here."""
        p, world = self.player, self.world
        stairs = world.floor.stairs_at(p.x, p.y)
        if stairs:
            self._use_stairs(stairs)
            self.turn += 1
        elif world.tile(p.x, p.y) == GRAIL:
            self._take_grail()
            self.turn += 1
        elif (p.x, p.y) in world.items:
            self._handled(*self.inventory.pick_up(world.items, (p.x, p.y)))
        else:
            self.log("There is nothing to use here.")

    def _use_stairs(self, stairs: str) -> None:
        world = self.world
        if stairs == NEXT:
            if world.floor_no + 1 not in world.visited:  # healed on the first visit only
                self.player.hp = min(PLAYER_HP, self.player.hp + HEAL_ON_CLIMB)
            world.enter(world.floor_no + 1, from_below=True, player=self.player)
            self.log(f"You climb to floor {world.floor_no}." if world.floor_no < TOTAL_FLOORS
                     else "The hall of the High Kings. The Lord is here.")
        elif stairs == BACK:
            world.enter(world.floor_no - 1, from_below=False, player=self.player)
            self.log(f"You go back down to floor {world.floor_no}.")

    def _take_grail(self) -> None:
        self.world.floor.tiles[self.player.y][self.player.x] = FLOOR
        self.inventory.add(GRAIL_NAME)
        self.won = True
        self.story.start(ENDING_PAGES, ENDING_HINT)

    def _story_over(self) -> None:
        if self.won:  # the ending is over: the world falls into chaos
            self.world.enter_chaos(self.player)
        if self.story.closing:
            self.log(self.story.closing)
        if self.world.chaos:
            self.log(THE_END)
