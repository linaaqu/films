from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from .database import init_db
from .routers import movies, reviews, auth

# ========== ROOT ==========
BASE_DIR = Path(__file__).resolve().parent.parent  # films/

INDEX_PATH = BASE_DIR / "frontend" / "index.html"

# ========== APP ==========
app = FastAPI(title="Фильмотека API", version="1.0.0")

# ========== DB ==========
@app.on_event("startup")
def startup():
    init_db()

# ========== CORS ==========
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== ROUTERS ==========
app.include_router(movies.router)
app.include_router(reviews.router)
app.include_router(auth.router)

# ========== STATIC ==========
POSTERS_DIR = BASE_DIR / "posters"

if POSTERS_DIR.exists():
    app.mount("/posters", StaticFiles(directory=POSTERS_DIR), name="posters")

# ========== SPA ==========
@app.get("/{path:path}")
async def spa(path: str):
    return FileResponse(INDEX_PATH)
