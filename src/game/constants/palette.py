"""All colors of the game. The client gets them from /palette (see routers/pages.py).

A triad of hues 120 degrees apart plus neutral greys. Colors can only be made with accent() or
neutral(), so nothing outside the scheme can be written; tests/test_palette.py checks the rest.
"""
import colorsys
from collections import namedtuple

RED, GREEN, BLUE = TRIAD = (8, 130, 245)
MAX_NEUTRAL_SATURATION = 15
MAX_ACCENT_SATURATION = 90 

Tier = namedtuple("Tier", "saturation lightness")


def _hex(hue: float, saturation: float, lightness: float) -> str:
    r, g, b = colorsys.hls_to_rgb(hue / 360, lightness / 100, saturation / 100)
    return f"#{round(r * 255):02x}{round(g * 255):02x}{round(b * 255):02x}"


def accent(hue: int, saturation: int, lightness: int) -> str:
    if hue not in TRIAD:
        raise ValueError(f"hue {hue} is not part of the triad")
    if saturation > MAX_ACCENT_SATURATION:
        raise ValueError(f"saturation {saturation} is above {MAX_ACCENT_SATURATION}")
    return _hex(hue, saturation, lightness)


def neutral(lightness: int, hue: int = 60, saturation: int = 0) -> str:
    if saturation > MAX_NEUTRAL_SATURATION:
        raise ValueError(f"saturation {saturation} is too colorful for a neutral")
    return _hex(hue, saturation, lightness)


def dim(color: str, factor: float = 0.45) -> str:
    return "#" + "".join(f"{round(int(color[i:i + 2], 16) * factor):02x}" for i in (1, 3, 5))


class Hues:
    RED, GREEN, BLUE = TRIAD
    MAX_NEUTRAL_SATURATION = MAX_NEUTRAL_SATURATION


class PageColors(Hues):
    BACKGROUND = neutral(7)
    TEXT = neutral(87)
    HEADER_TEXT = neutral(100)
    WALL = neutral(30, hue=BLUE - 5, saturation=11)
    FLOOR = neutral(50, saturation=7)
    DOOR = neutral(65, hue=30, saturation=14)


class CreatureColors(Hues):
    PLAYER = neutral(100)
    BOSS = accent(RED, 90, 66)
    MONSTER_TIERS = {1: Tier(45, 70), 2: Tier(58, 66), 3: Tier(70, 63), 4: Tier(82, 60), 5: Tier(90, 58)}

    @classmethod
    def monster(cls, hue: int, min_floor: int) -> str:
        tier = cls.MONSTER_TIERS[min_floor]
        lightness = tier.lightness + (14 if hue == BLUE else 0)  # blue looks darker than red or green
        return accent(hue, tier.saturation, lightness)


class LevelColors(PageColors):
    """Level glyphs as (seen, remembered)."""
    STAIRS = neutral(80)
    GRAIL = accent(BLUE, 90, 86)
    HEAD = accent(GREEN, 55, 78)
    BODY = accent(GREEN, 55, 66)
    HANDS = accent(GREEN, 55, 55)
    FEET = accent(GREEN, 55, 46)
    PILE = accent(GREEN, 25, 88)
    TILES = {
        ".": (PageColors.FLOOR, neutral(24, saturation=7)),
        "#": (PageColors.WALL, neutral(15, hue=BLUE - 5, saturation=11)),
        "=": (PageColors.DOOR, dim(PageColors.DOOR)),
        ">": (STAIRS, dim(STAIRS)),
        "<": (STAIRS, dim(STAIRS)),
        "Y": (GRAIL, dim(GRAIL)),
        "^": (HEAD, dim(HEAD)),
        "[": (BODY, dim(BODY)),
        "/": (HANDS, dim(HANDS)),
        "_": (FEET, dim(FEET)),
        "*": (PILE, dim(PILE)),
    }
    CHAOS = {"hues": list(TRIAD), "seen": "22% 62%", "remembered": "12% 26%"}


class MenuColors(LevelColors):
    TITLE = accent(BLUE, 60, 75)
    UI = {
        "title": TITLE,
        "heading": PageColors.TEXT,
        "item": LevelColors.BODY,
        "bright": neutral(100),
        "label": PageColors.FLOOR,
        "dim": neutral(40, saturation=5),
    }


class Palette(MenuColors, CreatureColors):
    @classmethod
    def for_client(cls) -> dict:
        return {
            "page": {"background": cls.BACKGROUND, "text": cls.TEXT, "header": cls.HEADER_TEXT, "border": cls.WALL},
            "tiles": {glyph: {"seen": seen, "remembered": remembered} for glyph, (seen, remembered) in cls.TILES.items()},
            "chaos": cls.CHAOS,
            "ui": cls.UI,
        }
