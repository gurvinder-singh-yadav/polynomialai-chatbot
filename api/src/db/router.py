from fastapi import APIRouter
from mongoengine import connect
from config import config

from .subroutes.users import router as users_router  
from .subroutes.agent import router as agent_router
router = APIRouter()

# Using a single connection with authentication
connect(
    db=config.MONGO_DB,
    username=config.MONGO_USERNAME,
    password=config.MONGO_PASSWORD,
    host=config.MONGO_HOST,
    port=int(config.MONGO_PORT),
    authentication_source='admin'  # Specify the authentication database
)

router.include_router(users_router)
router.include_router(agent_router)