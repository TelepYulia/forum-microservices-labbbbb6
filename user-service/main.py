import os
from fastapi import FastAPI, HTTPException

app = FastAPI(title="User Service - Variant 16")

STUDENT_N = 16

db_users = {
    1601: {"id": 1601, "username": "active_forum_user", "is_banned": False},
    1602: {"id": 1602, "username": "spammer", "is_banned": True}
}

@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    if user_id in db_users:
        user_data = db_users[user_id].copy()
        user_data["student_id"] = STUDENT_N
        return user_data
    raise HTTPException(status_code=404, detail="Користувача не знайдено")