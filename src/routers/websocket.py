import contextlib

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from game import Game

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(sock: WebSocket) -> None:
    await sock.accept()
    game = Game()  # one game per connection; the server is authoritative
    await sock.send_json(game.state())
    with contextlib.suppress(WebSocketDisconnect):
        while True:
            msg = await sock.receive_json()
            game.handle(str(msg.get("action", "")), msg.get("arg"))
            await sock.send_json(game.state())
