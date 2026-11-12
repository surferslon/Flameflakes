from fastapi import APIRouter
from fastapi.responses import FileResponse

from game.constants import Palette
from paths import STATIC

router = APIRouter()


@router.get("/")
async def index() -> FileResponse:
    return FileResponse(STATIC / "index.html")


@router.get("/palette")
async def colors() -> dict:
    return Palette.for_client()
