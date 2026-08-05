from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers import auth, journals, expenses, ai_agent, planner
import os

app = FastAPI(title="AI-Powered Travel Journal Assistant API")

# Fix CORS: Allow wildcard origins without credentials conflict
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads", exist_ok=True)
app.mount("/static", StaticFiles(directory="uploads"), name="static")

app.include_router(auth.router)
app.include_router(journals.router)
app.include_router(expenses.router)
app.include_router(ai_agent.router)
app.include_router(planner.router)

@app.get("/")
def read_root():
    return {"status": "Travel Journal API is operational"}
