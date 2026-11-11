from ..constants import LOG_LINES, LOG_TTL


class MessageLog:
    """The log lines under the level: newest first, a few at a time, each one fading after a while."""

    def __init__(self) -> None:
        self._lines: list[tuple[int, str, int]] = []  # (turn logged, text, id)
        self._seq = 0  # gives every line a unique id so the client can animate it

    def add(self, turn: int, text: str) -> None:
        self._seq += 1
        self._lines.insert(0, (turn, text, self._seq))
        del self._lines[LOG_LINES:]

    def visible(self, turn: int) -> list[tuple[int, str]]:
        """(id, text) of the lines that are still young enough to show."""
        return [(ident, text) for logged, text, ident in self._lines if turn - logged < LOG_TTL]
