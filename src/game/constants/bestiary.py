# Monsters. attack: their attack value, dv: their defense value (see HIT_BASE). min_floor / max_floor: the
# floors they appear on (no max_floor: all the way up); frequency: how common among those that can appear
# there. Damage is dice, speed 100 = one action per turn.
# Tuned so that a fight costs a player with the gear usually found on that floor a few HP, and so that
# weak monsters stop showing up once they are no threat any more. The hall of the top floor is hand-made.
MONSTERS = {
    "rat": {"ch": "r", "color": "#b9a089", "hp": 4, "damage": "1d4", "speed": 110, "attack": 35, "dv": 18, "min_floor": 1, "max_floor": 1, "frequency": 10},
    "ant": {"ch": "a", "color": "#d9783c", "hp": 5, "damage": "1d4", "speed": 100, "attack": 35, "dv": 8, "min_floor": 1, "max_floor": 1, "frequency": 10},
    "bug": {"ch": "b", "color": "#a3d84a", "hp": 3, "damage": "1d3", "speed": 90, "attack": 30, "dv": 4, "min_floor": 1, "max_floor": 1, "frequency": 8},
    "slime": {"ch": "j", "color": "#7fe0b0", "hp": 8, "damage": "1d4", "speed": 80, "attack": 30, "dv": 0, "min_floor": 1, "max_floor": 1, "frequency": 8},
    "goblin": {"ch": "g", "color": "#66cc66", "hp": 8, "damage": "1d6-1", "speed": 98, "attack": 40, "dv": 8, "min_floor": 1, "max_floor": 2, "frequency": 10},
    "bat": {"ch": "v", "color": "#8a7f9a", "hp": 4, "damage": "1d4", "speed": 130, "attack": 40, "dv": 25, "min_floor": 1, "max_floor": 1, "frequency": 7},
    "spider": {"ch": "s", "color": "#9a7bd1", "hp": 12, "damage": "1d6", "speed": 105, "attack": 50, "dv": 15, "min_floor": 2, "max_floor": 2, "frequency": 8},
    "gnome": {"ch": "n", "color": "#d6a15f", "hp": 14, "damage": "1d6", "speed": 90, "attack": 45, "dv": 5, "min_floor": 2, "max_floor": 2, "frequency": 8},
    "snake": {"ch": "S", "color": "#b5c93a", "hp": 10, "damage": "1d6", "speed": 100, "attack": 50, "dv": 12, "min_floor": 2, "max_floor": 2, "frequency": 6},
    "claw bug": {"ch": "c", "color": "#c2a14a", "hp": 10, "damage": "1d6", "speed": 105, "attack": 50, "dv": 12, "min_floor": 2, "max_floor": 3, "frequency": 6},
    "wolf": {"ch": "w", "color": "#a9b1bb", "hp": 16, "damage": "1d8-1", "speed": 120, "attack": 50, "dv": 15, "min_floor": 2, "max_floor": 3, "frequency": 6},
    "gremlin": {"ch": "G", "color": "#4fd1c5", "hp": 12, "damage": "1d6+2", "speed": 120, "attack": 55, "dv": 25, "min_floor": 3, "max_floor": 3, "frequency": 6},
    "witch": {"ch": "W", "color": "#c46bd6", "hp": 20, "damage": "2d4+1", "speed": 100, "attack": 60, "dv": 12, "min_floor": 3, "max_floor": 4, "frequency": 5},
    "skeleton": {"ch": "k", "color": "#e6e3d3", "hp": 22, "damage": "1d8+1", "speed": 95, "attack": 55, "dv": 10, "min_floor": 3, "max_floor": 4, "frequency": 6},
    "imp": {"ch": "i", "color": "#ff7a59", "hp": 14, "damage": "1d6+3", "speed": 115, "attack": 60, "dv": 20, "min_floor": 3, "max_floor": 3, "frequency": 5},
    "orc": {"ch": "o", "color": "#5f8f3a", "hp": 28, "damage": "1d8+1", "speed": 100, "attack": 55, "dv": 10, "min_floor": 3, "max_floor": 4, "frequency": 5},
    "hand": {"ch": "h", "color": "#e8c3a0", "hp": 22, "damage": "2d4+3", "speed": 110, "attack": 60, "dv": 10, "min_floor": 4, "max_floor": 5, "frequency": 5},
    "troll": {"ch": "T", "color": "#8a9a5b", "hp": 50, "damage": "2d6", "speed": 85, "attack": 55, "dv": 0, "min_floor": 4, "max_floor": 5, "frequency": 4},
    "zombie": {"ch": "z", "color": "#7a8f6a", "hp": 40, "damage": "2d6", "speed": 70, "attack": 45, "dv": 0, "min_floor": 4, "max_floor": 5, "frequency": 5},
    "ogre": {"ch": "O", "color": "#c98f6b", "hp": 45, "damage": "2d6+1", "speed": 90, "attack": 55, "dv": 5, "min_floor": 4, "max_floor": 5, "frequency": 3},
    "unicorn": {"ch": "u", "color": "#ffb3e6", "hp": 35, "damage": "2d8-1", "speed": 130, "attack": 70, "dv": 30, "min_floor": 5, "frequency": 3},
    "wraith": {"ch": "x", "color": "#9fb3ff", "hp": 30, "damage": "2d6+2", "speed": 115, "attack": 70, "dv": 28, "min_floor": 5, "frequency": 3},
    "golem": {"ch": "M", "color": "#a7c7d9", "hp": 70, "damage": "3d6-1", "speed": 75, "attack": 55, "dv": 5, "min_floor": 5, "frequency": 2},
    "elemental": {"ch": "E", "color": "#ffb020", "hp": 38, "damage": "2d8-1", "speed": 105, "attack": 70, "dv": 15, "min_floor": 5, "frequency": 3},
}

# What guards the hall of the top floor besides the boss (the hall is hand-made).
HALL_GUARDS = ("hand", "zombie", "troll", "ogre")

# The boss of the top floor. With the best gear a fight costs about a quarter of the player's hp;
# with the gear of the middle floors it is deadly.
BOSS = {"name": "Flake Lord", "ch": "F", "color": "#e55", "hp": 50, "damage": "2d6+8", "speed": 100,
        "attack": 75, "dv": 20}
