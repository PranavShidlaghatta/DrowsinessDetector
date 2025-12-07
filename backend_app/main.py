from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# NOTE: Very baad blanket CORS policy, make more specific later. 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SpeedPayload(BaseModel):
    speed_mph: float
    current_rpm: float 
# model for drowsiness score 
class PiScore(BaseModel):
    drowsiness_score: float

latest_speed_mph: float = 0.0

active_sockets: list[WebSocket] = []

async def broadcast_payload(payload: dict):
  for ws in list(active_sockets):
    try:
      await ws.send_json(payload)
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
    await broadcast_payload({"score" : score.drowsiness_score})
    return {"status": "success", "received_score": score.drowsiness_score}

@app.post("/speed")
async def update_speed(payload: SpeedPayload):
    global latest_speed_mph
    latest_speed_mph = payload.speed_mph
    rpm_percentage = payload.current_rpm
    # print(f"Received speed level: {latest_speed_mph}")
    print(f"Received rpm: {rpm_percentage}")
    await broadcast_payload({"speed_mph": latest_speed_mph})
    await broadcast_payload({"current_rpm" : rpm_percentage})
    return {"status": "ok"}

@app.get("/speed")
async def get_speed():
    return {"speed_mph": latest_speed_mph}

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