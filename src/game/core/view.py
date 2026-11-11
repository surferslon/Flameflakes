from ..constants import CARRY_CAPACITY, DEATH_MESSAGE, H, ITEMS, PILE_GLYPH, SLOT_GLYPHS, TOTAL_FLOORS, W


class ClientView:
    def __init__(self, game) -> None:
        self.game = game

    def state(self) -> dict:
        game, world, gear = self.game, self.game.world, self.game.inventory.gear
        shown = self._log_lines()
        return {
            "w": W, "h": H,
            # No level and no status line (black screen) during the intro pages and after death.
            "blank": (game.story.reading and not game.won) or game.dead,
            "level": world.level_id,
            "floor": "?" if world.chaos else world.floor_no, "floors": "?" if world.chaos else TOTAL_FLOORS,
            "map": self._known_map(),
            "visible": ["".join("1" if (x, y) in world.visible else "0" for x in range(W)) for y in range(H)],
            "entities": [{"id": e.id, "x": e.x, "y": e.y, "ch": e.ch, "color": e.color}
                         for e in (game.player, *world.monsters) if (e.x, e.y) in world.visible],
            "hp": max(game.player.hp, 0),
            "speed": game.player.speed, "damage": gear.damage, "pv": gear.pv, "dv": gear.dv,
            "equipment": dict(game.inventory.equipment), "backpack": list(game.inventory.backpack),
            "weight": game.inventory.weight, "capacity": CARRY_CAPACITY,
            "dead": game.dead,
            "won": game.won,
            "messages": [text for _, text in shown],
            "message_ids": [ident for ident, _ in shown],
        }

    def _known_map(self) -> list[str]:
        world = self.game.world
        known = [[tile if (x, y) in world.explored else " " for x, tile in enumerate(row)]
                 for y, row in enumerate(world.floor.tiles)]
        for (x, y), pile in world.items.items():  # items lying on a tile that has been seen
            if (x, y) in world.explored:
                known[y][x] = SLOT_GLYPHS[ITEMS[pile[0]]["slot"]] if len(pile) == 1 else PILE_GLYPH
        return ["".join(row) for row in known]

    def _log_lines(self) -> list[tuple[str, str]]:
        game = self.game
        if game.dead:  # the death message is all that is left on screen
            return [("death", DEATH_MESSAGE)]
        if game.story.reading:  # a story page is the only thing shown, and it has no turn
            return [(f"page:{game.story.current}", game.story.current)]
        return game.log_lines.visible(game.turn)
