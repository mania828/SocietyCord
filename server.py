from fastapi import FastAPI, WebSocket

app = FastAPI()
clients = set()

@app.get("/")
def home():
    return {"status": "SocietyCord online"}

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
    except:
        clients.discard(websocket)
