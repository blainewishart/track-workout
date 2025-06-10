from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Rep(BaseModel):
    count: int

class Set(BaseModel):
    start_time: datetime
    end_time: Optional[datetime] = None
    reps: List[int] = []

class Move(BaseModel):
    name: str
    weight: str
    set: Set

class Workout(BaseModel):
    start_time: datetime
    moves: List[Move] = []

# Initialize workout data
current_workout = Workout(start_time=datetime.now())

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

def serve_mockup():
    """Serve the static mockup HTML file"""
    mockup_path = Path("static/mockup.html")
    return HTMLResponse(mockup_path.read_text())

@app.get("/")
async def root():
    return serve_mockup()

@app.post("/api/move")
async def add_move(move: Move):
    current_workout.moves.append(move)
    return {"status": "success"}

@app.get("/api/workout")
async def get_workout():
    return current_workout

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 