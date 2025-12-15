
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from .ws import handle_ws

app = FastAPI()

@app.get("/")
async def index():
    with open("frontend/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.websocket("/ws/session/{session_id}")
async def websocket_endpoint(ws: WebSocket, session_id: str):
    await handle_ws(ws, session_id)
