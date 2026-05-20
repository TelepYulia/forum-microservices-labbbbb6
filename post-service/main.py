import os
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Post Service - Variant 16")

STUDENT_N = 16
START_ID = 100 * STUDENT_N  # 1600
id_counter = START_ID

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://localhost:8016")

class PostCreate(BaseModel):
    user_id: int
    content: str

@app.post("/api/posts")
def create_post(post: PostCreate):
    global id_counter


    try:
        response = httpx.get(f"{USER_SERVICE_URL}/api/users/{post.user_id}")
        if response.status_code == 404:
            raise HTTPException(status_code=400, detail="Користувача не існує")

        user_info = response.json()
        if user_info.get("is_banned"):
            raise HTTPException(status_code=403, detail="Користувач забанений")

    except httpx.RequestError:
        raise HTTPException(status_code=500, detail="User Service недоступний")

    id_counter += 1
    return {
        "status": "success",
        "data": {
            "post_id": id_counter,
            "user_id": post.user_id,
            "content": post.content
        },
        "student_id": STUDENT_N
    }