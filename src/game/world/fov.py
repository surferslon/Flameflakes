from ..constants import FOV_RADIUS
from .floor import Floor


def _line(x0: int, y0: int, x1: int, y1: int):
    """Bresenham line from (x0, y0) to (x1, y1), both ends included."""
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err = dx + dy
    while True:
        yield x0, y0
        if (x0, y0) == (x1, y1):
            return
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def visible_tiles(floor: Floor, ox: int, oy: int, radius: int = FOV_RADIUS) -> set[tuple[int, int]]:
    """Tiles the viewer at (ox, oy) can see. Walls block sight but are seen themselves."""
    seen = {(ox, oy)}
    for ty in range(max(0, oy - radius), min(floor.height, oy + radius + 1)):
        for tx in range(max(0, ox - radius), min(floor.width, ox + radius + 1)):
            if (tx - ox) ** 2 + (ty - oy) ** 2 > radius ** 2:
                continue
            path = list(_line(ox, oy, tx, ty))
            if all(floor.is_walkable(x, y) for x, y in path[1:-1]):
                seen.add((tx, ty))
    return seen
