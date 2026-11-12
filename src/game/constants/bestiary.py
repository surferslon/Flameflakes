from .palette import Palette

# Monsters. min_floor / max_floor: the floors they appear on; frequency: how common among those that can appear.
MONSTERS = {
    "rat": {"ch": "r", "color": Palette.monster(Palette.RED, 1), "hp": 4, "damage": "1d4", "speed": 110, "attack": 35, "dv": 18, "min_floor": 1, "max_floor": 1, "frequency": 10},
    "ant": {"ch": "a", "color": Palette.monster(Palette.RED, 1), "hp": 5, "damage": "1d4", "speed": 100, "attack": 35, "dv": 8, "min_floor": 1, "max_floor": 1, "frequency": 10},
    "bug": {"ch": "b", "color": Palette.monster(Palette.GREEN, 1), "hp": 3, "damage": "1d3", "speed": 90, "attack": 30, "dv": 4, "min_floor": 1, "max_floor": 1, "frequency": 8},
    "slime": {"ch": "j", "color": Palette.monster(Palette.GREEN, 1), "hp": 8, "damage": "1d4", "speed": 80, "attack": 30, "dv": 0, "min_floor": 1, "max_floor": 1, "frequency": 8},
    "goblin": {"ch": "g", "color": Palette.monster(Palette.GREEN, 1), "hp": 8, "damage": "1d6-1", "speed": 98, "attack": 40, "dv": 8, "min_floor": 1, "max_floor": 2, "frequency": 10},
    "bat": {"ch": "v", "color": Palette.monster(Palette.BLUE, 1), "hp": 4, "damage": "1d4", "speed": 130, "attack": 40, "dv": 25, "min_floor": 1, "max_floor": 1, "frequency": 7},
    "spider": {"ch": "s", "color": Palette.monster(Palette.BLUE, 2), "hp": 12, "damage": "1d6", "speed": 105, "attack": 50, "dv": 15, "min_floor": 2, "max_floor": 2, "frequency": 8},
    "gnome": {"ch": "n", "color": Palette.monster(Palette.RED, 2), "hp": 14, "damage": "1d6", "speed": 90, "attack": 45, "dv": 5, "min_floor": 2, "max_floor": 2, "frequency": 8},
    "snake": {"ch": "S", "color": Palette.monster(Palette.GREEN, 2), "hp": 10, "damage": "1d6", "speed": 100, "attack": 50, "dv": 12, "min_floor": 2, "max_floor": 2, "frequency": 6},
    "claw bug": {"ch": "c", "color": Palette.monster(Palette.RED, 2), "hp": 10, "damage": "1d6", "speed": 105, "attack": 50, "dv": 12, "min_floor": 2, "max_floor": 3, "frequency": 6},
    "wolf": {"ch": "w", "color": Palette.monster(Palette.RED, 2), "hp": 16, "damage": "1d8-1", "speed": 120, "attack": 50, "dv": 15, "min_floor": 2, "max_floor": 3, "frequency": 6},
    "gremlin": {"ch": "G", "color": Palette.monster(Palette.BLUE, 3), "hp": 12, "damage": "1d6+2", "speed": 120, "attack": 55, "dv": 25, "min_floor": 3, "max_floor": 3, "frequency": 6},
    "witch": {"ch": "W", "color": Palette.monster(Palette.BLUE, 3), "hp": 20, "damage": "2d4+1", "speed": 100, "attack": 60, "dv": 12, "min_floor": 3, "max_floor": 4, "frequency": 5},
    "skeleton": {"ch": "k", "color": Palette.monster(Palette.BLUE, 3), "hp": 22, "damage": "1d8+1", "speed": 95, "attack": 55, "dv": 10, "min_floor": 3, "max_floor": 4, "frequency": 6},
    "imp": {"ch": "i", "color": Palette.monster(Palette.RED, 3), "hp": 14, "damage": "1d6+3", "speed": 115, "attack": 60, "dv": 20, "min_floor": 3, "max_floor": 3, "frequency": 5},
    "orc": {"ch": "o", "color": Palette.monster(Palette.GREEN, 3), "hp": 28, "damage": "1d8+1", "speed": 100, "attack": 55, "dv": 10, "min_floor": 3, "max_floor": 4, "frequency": 5},
    "hand": {"ch": "h", "color": Palette.monster(Palette.RED, 4), "hp": 22, "damage": "2d4+3", "speed": 110, "attack": 60, "dv": 10, "min_floor": 4, "max_floor": 5, "frequency": 5},
    "troll": {"ch": "T", "color": Palette.monster(Palette.GREEN, 4), "hp": 50, "damage": "2d6", "speed": 85, "attack": 55, "dv": 0, "min_floor": 4, "max_floor": 5, "frequency": 4},
    "zombie": {"ch": "z", "color": Palette.monster(Palette.GREEN, 4), "hp": 40, "damage": "2d6", "speed": 70, "attack": 45, "dv": 0, "min_floor": 4, "max_floor": 5, "frequency": 5},
    "ogre": {"ch": "O", "color": Palette.monster(Palette.RED, 4), "hp": 45, "damage": "2d6+1", "speed": 90, "attack": 55, "dv": 5, "min_floor": 4, "max_floor": 5, "frequency": 3},
    "unicorn": {"ch": "u", "color": Palette.monster(Palette.BLUE, 5), "hp": 35, "damage": "2d8-1", "speed": 130, "attack": 70, "dv": 30, "min_floor": 5, "frequency": 3},
    "wraith": {"ch": "x", "color": Palette.monster(Palette.BLUE, 5), "hp": 30, "damage": "2d6+2", "speed": 115, "attack": 70, "dv": 28, "min_floor": 5, "frequency": 3},
    "golem": {"ch": "M", "color": Palette.monster(Palette.BLUE, 5), "hp": 70, "damage": "3d6-1", "speed": 75, "attack": 55, "dv": 5, "min_floor": 5, "frequency": 2},
    "elemental": {"ch": "E", "color": Palette.monster(Palette.RED, 5), "hp": 38, "damage": "2d8-1", "speed": 105, "attack": 70, "dv": 15, "min_floor": 5, "frequency": 3},
}

HALL_GUARDS = ("hand", "zombie", "troll", "ogre")

BOSS = {"name": "Flake Lord", "ch": "F", "color": Palette.BOSS, "hp": 50, "damage": "2d6+8", "speed": 100,
        "attack": 75, "dv": 20}
