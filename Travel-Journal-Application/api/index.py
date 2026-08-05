import sys
import os

# Add backend directory to sys.path so app module can be imported properly by Vercel
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.main import app

# Export ASGI application for Vercel Serverless Execution
handler = app
