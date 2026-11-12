"""The map, the tower and what can be seen."""

W, H = 60, 21
WALL, FLOOR, DOOR = "#", ".", "="
NEXT, BACK = ">", "<"
GRAIL = "Y"
GRAIL_NAME = "Cursed Grail of Chaos"
CHAOS_EXCLUDED = set("#.=<>Y@ ")

FOV_RADIUS = 8
SIGHT = 8

TOTAL_FLOORS = 6
LOOT_PER_FLOOR = 4
