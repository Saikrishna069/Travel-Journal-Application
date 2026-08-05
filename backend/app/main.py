from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers import auth, journals, expenses, ai_agent, planner
import os

app = FastAPI(
    title="AI-Powered Travel Journal Assistant API",
    redirect_slashes=False
)

# Universal CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads", exist_ok=True)
app.mount("/static", StaticFiles(directory="uploads"), name="static")

# Include Routers
app.include_router(auth.router)
app.include_router(journals.router)
app.include_router(expenses.router)
app.include_router(ai_agent.router)
app.include_router(planner.router)

@app.api_route("/", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def read_root():
    return {"status": "Travel Journal API is operational"}
