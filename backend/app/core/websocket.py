from fastapi import WebSocket
from typing import List
import logging

logger = logging.getLogger(__name__)

class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        try:
            await websocket.accept()
            self.active_connections.append(websocket)
            logger.info(f"New WebSocket connection. Total connections: {len(self.active_connections)}")
        except Exception as e:
            logger.error(f"Failed to connect WebSocket: {str(e)}")
            raise

    async def disconnect(self, websocket: WebSocket):
        try:
            self.active_connections.remove(websocket)
            logger.info(f"WebSocket disconnected. Remaining connections: {len(self.active_connections)}")
        except ValueError:
            logger.warning("Attempted to disconnect WebSocket that wasn't connected")
        except Exception as e:
            logger.error(f"Error during WebSocket disconnection: {str(e)}")
    
    async def broadcast(self, message: dict):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Failed to send message to WebSocket: {str(e)}")
                disconnected.append(connection)
        
        # Clean up disconnected connections
        for conn in disconnected:
            await self.disconnect(conn)

manager = WebSocketManager()