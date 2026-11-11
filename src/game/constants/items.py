"""Things to wear and wield, and how they look when they lie on the floor."""


from .world import GRAIL_NAME

# Items. slot: where it is worn; weight in kg. Effects, all optional:
#   damage  dice rolled per hit (Hands)           pv     protection value: taken off every hit you suffer
#   dv      defense value: how hard you are to hit (heavy gear can have a negative one)
#   hit     accuracy bonus for your own attacks   speed  added to your speed
# Items with min_floor and frequency also lie around on the floors; the rest are only carried from the start.
HANDS_ITEMS = {
    "Knife":        {"slot": "Hands", "damage": "1d6", "hit": 0,  "dv": 0, "weight": 0.5, "min_floor": 1, "frequency": 1},
    "Dagger":       {"slot": "Hands", "damage": "2d5", "hit": 10, "dv": 3, "weight": 1},
    "Short Sword":  {"slot": "Hands", "damage": "3d4", "hit": 5,  "dv": 2, "weight": 2,   "min_floor": 1, "frequency": 6},
    "Axe":          {"slot": "Hands", "damage": "2d8", "hit": 0,  "dv": 0, "weight": 3,   "min_floor": 2, "frequency": 5},
    "Mace":         {"slot": "Hands", "damage": "3d6", "hit": -5, "dv": -1, "weight": 4.5, "min_floor": 3, "frequency": 4},
    "Great Sword":  {"slot": "Hands", "damage": "4d6", "hit": -10, "dv": -2, "weight": 7,  "min_floor": 4, "frequency": 2},
    "Kriegsmesser":  {"slot": "Hands", "damage": "4d6", "hit": -10, "dv": -2, "weight": 7,  "min_floor": 5, "frequency": 1},
}

HEAD_ITEMS = {
    "Wool Hat":     {"slot": "Head", "pv": 0, "dv": 0, "weight": 0.2},
    "Leather Cap":  {"slot": "Head", "pv": 1, "dv": 1, "weight": 0.5, "min_floor": 1, "frequency": 6},
    "Iron Helmet":  {"slot": "Head", "pv": 2, "dv": -1, "weight": 1.5, "min_floor": 2, "frequency": 5},
    "Horned Helm":  {"slot": "Head", "pv": 3, "dv": -2, "weight": 2.5, "min_floor": 4, "frequency": 3},
}

BODY_ITEMS = {
    "Fur":          {"slot": "Body", "pv": 1, "dv": 0, "weight": 3},
    "Leather Jerkin": {"slot": "Body", "pv": 2, "dv": 0, "weight": 3.5, "min_floor": 1, "frequency": 6},
    "Chainmail":    {"slot": "Body", "pv": 4, "dv": -5, "weight": 8,  "min_floor": 3, "frequency": 4},
    "Plate Armor":  {"slot": "Body", "pv": 6, "dv": -10, "weight": 14, "min_floor": 5, "frequency": 1},
}

FEET_ITEMS = {
    "Leather Shoes": {"slot": "Feet", "pv": 0, "dv": 1, "weight": 1},
    "Boots":        {"slot": "Feet", "pv": 1, "dv": 2, "weight": 1.5, "min_floor": 1, "frequency": 6},
    "Iron Boots":   {"slot": "Feet", "pv": 2, "dv": -2, "weight": 3,  "min_floor": 3, "frequency": 3},
    "Swift Boots":  {"slot": "Feet", "speed": 15, "dv": 8, "weight": 1, "min_floor": 2, "frequency": 3},
}

OTHER_ITEMS = {GRAIL_NAME: {"weight": 2}}

ITEMS = HANDS_ITEMS | HEAD_ITEMS | BODY_ITEMS | FEET_ITEMS | OTHER_ITEMS

SLOT_GLYPHS = {"Head": "^", "Body": "[", "Hands": "/", "Feet": "_"}   # how items lying on the floor look
PILE_GLYPH = "*"                              # several items lying on one tile
