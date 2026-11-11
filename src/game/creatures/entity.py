import itertools
from dataclasses import dataclass, field

from ..constants import ACTION_COST, DEFAULT_SPEED

_ids = itertools.count(1)


@dataclass
class Entity:
    x: int
    y: int
    ch: str
    color: str
    name: str
    hp: int
    ai: bool = False
    damage: str = "1d3"  # dice rolled per hit, e.g. "2d6"
    boss: bool = False
    attack: int = 40             # attack value: rolls against the DV of the target (see combat.py)
    dv: int = 0                  # defense value: how hard it is to hit
    speed: int = DEFAULT_SPEED   # energy gained per turn; acts whenever it reaches ACTION_COST
    energy: float | None = None  # filled in below
    id: int = field(default_factory=lambda: next(_ids))  # stable identity for client animation

    def __post_init__(self) -> None:
        if self.energy is None:
            self.energy = max(0, ACTION_COST - self.speed)
