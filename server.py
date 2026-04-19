from fastapi import FastAPI, WebSocket
import asyncio
import time
app = FastAPI()
clients = set()

@app.get("/")
def home():
    return {"status": "online"}

@app.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)

    try:
        while True:
            msg = await websocket.receive_text()

            for c in list(clients):
                try:
                    await c.send_text(msg)
                except:
                    clients.discard(c)

    except Exception as e:
        print("WebSocket error:", e)

    finally:
        clients.discard(websocket)

@app.get("/ping")
def ping():
    return {"time": time.time()}