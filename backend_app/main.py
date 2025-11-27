from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI()

# NOTE: Blanket CORS policy, make more specific later. 
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

@app.get("/")
async def root():
    return {"status" : "success", "on root" : "yes"} 

@app.post("/piRunner")
async def get_heuristic(score: PiScore):
    """
    Receives drowsiness score as json from Raspberry Pi.
    """
    print(f"Received drowsiness score: {score.drowsiness_score:.2f}", flush=True)
    return {"status": "success", "received_score": score.drowsiness_score}


@app.get("/status")
async def status():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)