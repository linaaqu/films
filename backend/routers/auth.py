from fastapi import APIRouter, HTTPException
from ..database import get_db_connection

router = APIRouter(tags=["auth"])

@router.post("/register")
async def register(name: str, email: str, password: str):
    if len(password) < 4:
        raise HTTPException(400, "Пароль минимум 4 символа")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    existing = cursor.fetchone()
    if existing:
        conn.close()
        raise HTTPException(400, "Email уже зарегистрирован")
    
    cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
    conn.commit()
    conn.close()
    return {"message": "Регистрация успешна"}

@router.post("/login")
async def login(email: str, password: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, password FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()
    conn.close()
    if not row or row[3] != password:
        raise HTTPException(401, "Неверный email или пароль")
    return {"user": {"id": row[0], "name": row[1], "email": row[2]}, "message": "Вход выполнен"}
