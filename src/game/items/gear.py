from ..constants import BASE_ATTACK, BASE_DV, ITEMS, UNARMED_DAMAGE


class Gear:
    def __init__(self, equipment: dict[str, str | None]) -> None:
        self._equipment = equipment  # slot -> item name; shared with the inventory

    def _total(self, key: str) -> int:
        return sum(ITEMS[name].get(key, 0) for name in self._equipment.values() if name)

    @property
    def damage(self) -> str:
        weapon = self._equipment["Hands"]
        return ITEMS[weapon]["damage"] if weapon else UNARMED_DAMAGE

    @property
    def attack(self) -> int:
        return BASE_ATTACK + self._total("hit")

    @property
    def pv(self) -> int:
        return self._total("pv")

    @property
    def dv(self) -> int:
        return BASE_DV + self._total("dv")

    @property
    def speed_bonus(self) -> int:
        return self._total("speed")
