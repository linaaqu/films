from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from .database import init_db
from .routers import movies, reviews, auth

# 1. Сначала создаём приложение
app = FastAPI(title="Фильмотека API", version="1.0.0")

# 2. Потом инициализируем БД 
@app.on_event("startup")
def startup():
    init_db()

# 3. CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Роутеры
app.include_router(movies.router)
app.include_router(reviews.router)
app.include_router(auth.router)

# 5. Статика (только постеры)
app.mount("/posters", StaticFiles(directory="posters"), name="posters")

# 6. Базовая директория 
BASE_DIR = Path(__file__).resolve().parent

# 7. ЧПУ для фронтенда 
@app.get("/{full_path:path}")
def serve_frontend(full_path: str):
    return FileResponse(BASE_DIR / "index.html")
