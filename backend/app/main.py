from fastapi import FastAPI
from app.api.endpoints import news
from fastapi.middleware.cors import CORSMiddleware
import logging
from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect
from app.core.websocket import manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(news.router, prefix="/api/news", tags=["news"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_json({"message": "received"})
    except WebSocketDisconnect:
        pass