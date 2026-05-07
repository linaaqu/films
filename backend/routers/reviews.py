from fastapi import APIRouter, HTTPException
from ..database import get_db_connection

router = APIRouter(tags=["reviews"])

@router.get("/{movie_id}")
async def get_reviews(movie_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.*, COALESCE(u.name, r.author_name, 'Аноним') as author_name
        FROM reviews r
        LEFT JOIN users u ON r.user_id = u.id
        WHERE r.movie_id = ?
        ORDER BY r.created_at DESC
    """, (movie_id,))
    rows = cursor.fetchall()
    conn.close()
    
    result = []
    for r in rows:
        result.append({
            "id": r[0],
            "movie_id": r[1],
            "user_id": r[2],
            "rating": r[3],
            "comment": r[4],
            "created_at": r[5],
            "author_name": r[6] if len(r) > 6 else "Аноним"
        })
    
    # Если нет отзывов, возвращаем примерные для демонстрации
    if len(result) == 0:
        result = [
            {"id": 1, "movie_id": movie_id, "user_id": 1, "rating": 9, "comment": "Потрясающий фильм! Очень понравился сюжет и игра актёров. Рекомендую всем к просмотру!", "created_at": "2024-01-15", "author_name": "Алексей"},
            {"id": 2, "movie_id": movie_id, "user_id": 2, "rating": 8, "comment": "Отличная картина, особенно впечатлили визуальные эффекты. Немного затянуто, но в целом здорово!", "created_at": "2024-01-20", "author_name": "Мария"}
        ]
    
    return result

@router.post("/")
async def create_review(movie_id: int, rating: int, comment: str, user_id: int = 1, author: str = None):
    if rating < 1 or rating > 10:
        raise HTTPException(400, "Оценка от 1 до 10")
    if not comment:
        raise HTTPException(400, "Комментарий не может быть пустым")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Добавляем поле author_name в таблицу, если его нет
    try:
        cursor.execute("ALTER TABLE reviews ADD COLUMN author_name TEXT")
    except:
        pass
    
    author_name = author or "Аноним"
    
    cursor.execute("""
        INSERT INTO reviews (movie_id, user_id, rating, comment, author_name)
        VALUES (?, ?, ?, ?, ?)
    """, (movie_id, user_id, rating, comment, author_name))
    conn.commit()
    conn.close()
    return {"message": "Отзыв добавлен"}
