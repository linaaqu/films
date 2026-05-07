from fastapi import APIRouter, HTTPException
from ..database import get_db_connection

router = APIRouter(prefix="/api/movies", tags=["movies"])

@router.get("/")
async def get_movies():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, title, genre, year, rating, description, duration_min, age_rating, country, director, actors, poster FROM movies ORDER BY id")
        rows = cursor.fetchall()
    except Exception as e:
        conn.close()
        raise HTTPException(500, f"Ошибка базы данных: {str(e)}")
    
    conn.close()
    
    result = []
    for r in rows:
        result.append({
            "id": r[0],
            "title": r[1] if r[1] else "",
            "genre": r[2] if r[2] else "",
            "year": r[3] if r[3] else 0,
            "rating": float(r[4]) if r[4] else 0,
            "description": r[5] if r[5] else "",
            "duration_min": r[6] if r[6] else None,
            "age_rating": r[7] if r[7] else "",
            "country": r[8] if r[8] else "",
            "director": r[9] if r[9] else "",
            "actors": r[10].split(",") if r[10] else [],
            "poster": r[11] if len(r) > 11 and r[11] else "posters/default.webp"
        })
    return result

@router.get("/{movie_id}")
async def get_movie(movie_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies WHERE id = ?", (movie_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(404, "Фильм не найден")
    return {
        "id": row[0],
        "title": row[1],
        "genre": row[2],
        "year": row[3],
        "rating": row[4],
        "description": row[5] if row[5] else "",
        "duration_min": row[6],
        "age_rating": row[7],
        "country": row[8],
        "director": row[9] if len(row) > 9 else "",
        "actors": row[10].split(",") if len(row) > 10 and row[10] else [],
        "poster": row[11] if len(row) > 11 and row[11] else "posters/default.webp"
    }
