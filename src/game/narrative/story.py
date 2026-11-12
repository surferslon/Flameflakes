class Story:
    """Pages of story text. While there are pages left the game waits for Enter on each of them."""

    def __init__(self, pages: list[str] | None = None, closing: str = "") -> None:
        self.pages: list[str] = list(pages or [])
        self.closing = closing

    def start(self, pages: list[str], closing: str = "") -> None:
        self.pages, self.closing = list(pages), closing

    @property
    def reading(self) -> bool:
        return bool(self.pages)

    @property
    def current(self) -> str:
        return self.pages[0]

    def confirm(self) -> bool:
        self.pages.pop(0)
        return not self.pages
