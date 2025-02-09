import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_websocket_connection():
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        data = {"type": "test"}
        websocket.send_json(data)
        response = websocket.receive_json()
        assert response is not None