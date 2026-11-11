from ..constants import CARRY_CAPACITY, EQUIPMENT_SLOTS, ITEMS, START_ITEMS
from .gear import Gear

Pos = tuple[int, int]
Result = tuple[bool, list[str]]  # whether something happened, and what the log should say


def pile_text(pile: list[str]) -> str:
    """What the log says when the player stands on items lying on the floor."""
    if len(pile) == 1:
        return f"{pile[0]} lies here. Press F to pick it up."
    return "Several items lying here. Press F to pick one up."


class Inventory:
    def __init__(self) -> None:
        self.equipment: dict[str, str | None] = dict.fromkeys(EQUIPMENT_SLOTS)  # slot -> item name
        self.backpack: list[str] = []  # item names; carried, not worn
        for name in START_ITEMS:
            self.equipment[ITEMS[name]["slot"]] = name
        self.gear = Gear(self.equipment)

    @property
    def weight(self) -> float:
        names = [*self.equipment.values(), *self.backpack]
        return round(sum(ITEMS[name]["weight"] for name in names if name), 2)

    def fits(self, extra_weight: float) -> bool:
        return self.weight + extra_weight <= CARRY_CAPACITY

    def add(self, name: str) -> None:
        self.backpack.append(name)

    def equip(self, index: object) -> Result:
        """Wear the backpack item at `index`; whatever was worn there goes into the backpack."""
        if not isinstance(index, int) or not 0 <= index < len(self.backpack):
            return False, []
        name = self.backpack[index]
        slot = ITEMS[name].get("slot")
        if not slot:
            return False, [f"The {name} cannot be worn."]
        old, self.equipment[slot] = self.equipment[slot], name  # the total weight stays the same
        if old:
            self.backpack[index] = old
            return True, [f"You swap the {old} for the {name}."]
        del self.backpack[index]
        return True, [f"You put on the {name}."]

    def unequip(self, slot: object) -> Result:
        name = self.equipment.get(slot) if isinstance(slot, str) else None
        if not name:
            return False, []
        self.equipment[slot] = None
        self.backpack.append(name)
        return True, [f"You take off the {name}."]

    def pick_up(self, items: dict[Pos, list[str]], pos: Pos) -> Result:
        """Take the item on top of the pile at `pos` (the one put down last)."""
        pile = items[pos]
        name = pile[-1]
        if not self.fits(ITEMS[name]["weight"]):
            return False, [f"The {name} is too heavy for you to carry."]
        pile.pop()
        if not pile:
            del items[pos]
        self.add(name)
        return True, [f"You pick up the {name}.", *([pile_text(pile)] if pile else [])]

    def drop(self, items: dict[Pos, list[str]], pos: Pos, index: object) -> Result:
        """Put the backpack item at `index` down on the pile at `pos`."""
        if not isinstance(index, int) or not 0 <= index < len(self.backpack):
            return False, []
        name = self.backpack.pop(index)
        items.setdefault(pos, []).append(name)
        return True, [f"You drop the {name}."]
