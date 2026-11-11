from fastapi import APIRouter
from fastapi.responses import FileResponse

from paths import STATIC

router = APIRouter()


@router.get("/")
async def index() -> FileResponse:
    return FileResponse(STATIC / "index.html")
