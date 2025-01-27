from fastapi import APIRouter
from config import config

router = APIRouter()

@router.get("/users")
async def get_users():
    return {f"message": f"Hello, World! {config.SUPERUSER_EMAIL} {config.SUPERUSER_PASSWORD}"}
