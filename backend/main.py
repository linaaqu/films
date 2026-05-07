from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .database import init_db
from .routers import movies, reviews, auth

# Инициализация базы данных при запуске
init_db()

app = FastAPI(title="Фильмотека API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== СТАТИЧЕСКИЕ ФАЙЛЫ (ДОЛЖНЫ БЫТЬ ПЕРВЫМИ!) ==========
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

app.mount("/static", StaticFiles(directory=BASE_DIR), name="static")
app.mount("/posters", StaticFiles(directory=BASE_DIR / "posters"), name="posters")

# Подключаем роутеры API
app.include_router(movies.router)
app.include_router(reviews.router)
app.include_router(auth.router)

# Статические файлы CSS/JS
@app.get("/style.css")
async def get_css():
    return FileResponse("style.css")

@app.get("/app.js")
async def get_js():
    return FileResponse("app.js")

# ========== ЧПУ МАРШРУТЫ  ==========
@app.get("/")
@app.get("/movies")
@app.get("/favorites")
@app.get("/profile")
@app.get("/login")
@app.get("/register")
@app.get("/movie/{movie_id}")
async def serve_frontend(movie_id: int = None):
    """Отдаёт index.html для всех маршрутов ЧПУ"""
    return FileResponse("index.html")

import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
