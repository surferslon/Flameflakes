from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from paths import STATIC
from routers import pages, websocket

app = FastAPI()
app.include_router(pages.router)
app.include_router(websocket.router)
app.mount("/static", StaticFiles(directory=STATIC), name="static")
