"""Every color must follow the scheme in src/game/constants/palette.py: the triad plus neutrals."""
import colorsys
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from game.constants import MONSTERS, Palette  # noqa: E402

BACKGROUND, RED, GREEN, BLUE = Palette.BACKGROUND, Palette.RED, Palette.GREEN, Palette.BLUE
PLAYER, BOSS_COLOR = Palette.PLAYER, Palette.BOSS
MAX_NEUTRAL_SATURATION = Palette.MAX_NEUTRAL_SATURATION
palette = Palette.for_client

HUE_TOLERANCE = 10
MIN_CONTRAST = 3.0  # WCAG for large text; every glyph is drawn at 32 px bold


def _rgb(color):
    return [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]


def _hls(color):
    h, l, s = colorsys.rgb_to_hls(*_rgb(color))
    return h * 360, l, s


def _luminance(color):
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in _rgb(color)]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def _contrast(a, b):
    hi, lo = sorted((_luminance(a), _luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def _all_colors():
    p = palette()
    yield from ((f"page.{k}", v) for k, v in p["page"].items())
    for glyph, modes in p["tiles"].items():
        yield from ((f"tile {glyph} {mode}", c) for mode, c in modes.items())
    yield from ((f"ui.{k}", v) for k, v in p["ui"].items())
    yield "player", PLAYER
    yield "boss", BOSS_COLOR
    yield from ((f"monster {name}", m["color"]) for name, m in MONSTERS.items())


def test_every_color_is_in_the_triad_or_neutral():
    for name, color in _all_colors():
        hue, _, saturation = _hls(color)
        if saturation * 100 <= MAX_NEUTRAL_SATURATION:
            continue
        distance = min(min(abs(hue - t), 360 - abs(hue - t)) for t in (RED, GREEN, BLUE))
        assert distance <= HUE_TOLERANCE, f"{name} {color}: hue {hue:.0f} is not in the triad"


def test_items_are_green():
    for glyph in "^[/_*":
        assert abs(_hls(palette()["tiles"][glyph]["seen"])[0] - GREEN) <= HUE_TOLERANCE, glyph


def test_glyphs_and_text_are_readable_on_the_background():
    p = palette()
    readable = [(f"tile {g}", m["seen"]) for g, m in p["tiles"].items() if g != "#"]
    readable += [(f"ui.{k}", v) for k, v in p["ui"].items()]
    readable += [("player", PLAYER), ("boss", BOSS_COLOR)] + [(n, m["color"]) for n, m in MONSTERS.items()]
    for name, color in readable:
        assert _contrast(color, BACKGROUND) >= MIN_CONTRAST, f"{name} {color}: contrast {_contrast(color, BACKGROUND):.1f}"


def test_remembered_tiles_are_darker_than_seen_ones():
    for glyph, modes in palette()["tiles"].items():
        assert _luminance(modes["remembered"]) < _luminance(modes["seen"]), glyph


def test_no_color_literals_outside_the_palette():
    patterns = [r"#[0-9a-fA-F]{3,8}\b", r"\b(?:rgb|rgba|hsl|hsla)\(\s*\d"]
    files = [f for pattern in ("static/**/*.js", "static/**/*.css", "static/**/*.html") for f in ROOT.glob(pattern)]
    py = [f for f in (ROOT / "src").rglob("*.py") if f.name != "palette.py"]
    for f in files + py:
        text = f.read_text()
        if f in py:  # in Python only string literals count; "#abc" in a comment does not
            text = "\n".join(re.findall(r"[\"']#[0-9a-fA-F]{3,8}[\"']", text))
        for pattern in patterns:
            assert not re.search(pattern, text), f"{f.relative_to(ROOT)} defines a color; move it to palette.py"
