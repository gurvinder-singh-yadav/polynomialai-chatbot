from fastapi import APIRouter
from ..schemas import MessageUpdate, UserCreate, UserCreateResponse, UserResponse
from config import config
from ..models import User, Message
from pprint import pprint
from datetime import datetime, timezone

router = APIRouter()

@router.get("/chats", response_model=list[dict])
async def get_users():
    users = User.objects.all()
    result = []
    for user in users:
        user_dict = user.to_mongo().to_dict()
        # Convert ObjectId to string
        user_dict['_id'] = str(user_dict['_id'])
        result.append(user_dict)
    return result

@router.post("/users", response_model=UserCreateResponse)
async def create_user():
    user_dict = {}
    # Convert string dates to datetime objects
    user_dict['created_at'] = datetime.now(timezone.utc)
    user_dict['updated_at'] = datetime.now(timezone.utc)
    user_dict['messages'] = []
    
    user = User(**user_dict)
    user.save()
    return UserResponse(
        id=user.id, 
        created_at=user.created_at, 
        updated_at=user.updated_at,
        messages=user.messages  # Include messages in the response
    )

@router.put("/users/{user_id}")
async def update_user(user_id: str, messages: MessageUpdate):
    user = User.objects.get(id=user_id)
    # Create proper Message documents for MongoDB
    new_messages = []
    for message in messages.messages:
        new_messages.append(Message(content=message.content, role=message.role, created_at=message.created_at))
    
    # Update the messages list
    if not user.messages:
        user.messages = new_messages
    else:
        user.messages.extend(new_messages)
    
    user.updated_at = datetime.now(timezone.utc)
    user.save()
    return {"message": "user is updated"}
