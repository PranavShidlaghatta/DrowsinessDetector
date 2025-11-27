from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# NOTE: Very bad blanket CORS policy, make more specific later. 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# model for drowsiness score 
class PiScore(BaseModel):
    drowsiness_score: float

active_sockets: list[WebSocket] = []

async def broadcast_score(score: float):
  for ws in list(active_sockets):
    try:
      await ws.send_json({"score": score})
    except Exception:
      # drop dead sockets
      active_sockets.remove(ws)

@app.get("/")
async def root():
    return {"status" : "success", "on root" : "yes"} 

@app.post("/piRunner")
async def get_heuristic(score: PiScore):
    """
    Receives drowsiness score as json from Raspberry Pi.
    """
    print(f"Received drowsiness score: {score.drowsiness_score:.2f}", flush=True)
    await broadcast_score(score.drowsiness_score)
    return {"status": "success", "received_score": score.drowsiness_score}

@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_sockets.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_sockets.remove(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)