"""The map, the tower and what can be seen."""

W, H = 60, 21                                 # floor size in tiles
WALL, FLOOR = "#", "."
NEXT, BACK = ">", "<"                         # stairs to the next floor up / back to the floor below
GRAIL = "Y"                                   # the Cursed Grail of Chaos: taking it wins the game
GRAIL_NAME = "Cursed Grail of Chaos"
CHAOS_EXCLUDED = set("#.<>Y@ ")                # glyphs with a meaning of their own

# Perception
FOV_RADIUS = 8                                # how far the player sees
SIGHT = 8                                     # how close the player must be for monsters to notice

TOTAL_FLOORS = 6
LOOT_PER_FLOOR = 4                            # items lying around on each generated floor
