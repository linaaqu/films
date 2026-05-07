from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from .database import init_db
from .routers import movies, reviews, auth

BASE_DIR = Path(__file__).resolve().parent.parent

# Абсолютный путь к frontend
FRONTEND_DIR = BASE_DIR / "frontend"
INDEX_PATH = BASE_DIR / "frontend" / "index.html"

app = FastAPI(title="Фильмотека API", version="1.0.0")

# DB
@app.on_event("startup")
def startup():
    init_db()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== API РОУТЫ (ЕДИНООБРАЗНЫЕ ПРЕФИКСЫ) ==========
app.include_router(movies.router, prefix="/api/movies")
app.include_router(reviews.router, prefix="/api/reviews")
app.include_router(auth.router, prefix="/api/auth")

# ========== СТАТИКА ==========
# CSS, JS из папки frontend
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# Постеры
POSTERS_DIR = BASE_DIR / "posters"
if POSTERS_DIR.exists():
    app.mount("/posters", StaticFiles(directory=POSTERS_DIR), name="posters")

# ========== ГЛАВНАЯ СТРАНИЦА ==========
@app.get("/")
async def root():
    return FileResponse(INDEX_PATH)

# ========== SPA FALLBACK ==========
@app.get("/{full_path:path}")
async def spa(full_path: str):
    # Не трогаем API, статику и постеры
    if full_path.startswith(("api", "static", "posters")):
        return {"detail": "Not found"}
    return FileResponse(INDEX_PATH)
