from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from .database import init_db
from .routers import movies, reviews, auth

# ========== БАЗОВАЯ ДИРЕКТОРИЯ ==========
BASE_DIR = Path(__file__).resolve().parent  # backend/

# ==========  ПРИЛОЖЕНИЕ ==========
app = FastAPI(title="Фильмотека API", version="1.0.0")

# ========== БАЗА ДАННЫХ ==========
@app.on_event("startup")
def startup():
    init_db()

# ==========  CORS ==========
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== РОУТЕРЫ API ==========
app.include_router(movies.router)
app.include_router(reviews.router)
app.include_router(auth.router)

# ========== СТАТИКА (постеры) ==========
POSTERS_DIR = BASE_DIR / "posters"
app.mount("/posters", StaticFiles(directory=POSTERS_DIR), name="posters")

# ==========  SPA FALLBACK (==========
@app.get("/{path:path}")
async def spa(path: str):
    if path.startswith("posters") or path.startswith("docs") or path.startswith("openapi"):
        return {"error": "not found"}
    return FileResponse(BASE_DIR / "index.html")
