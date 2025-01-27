from fastapi import APIRouter

from src.subroutes.users import router as users_router  

router = APIRouter()

router.include_router(users_router)
