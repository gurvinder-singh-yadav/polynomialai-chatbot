from datetime import datetime, timezone
from fastapi import APIRouter
from ..utils import Agent
from ..schemas import Message

router = APIRouter()
agent = Agent()



@router.post("/agent", response_model=Message)
async def get_agent(msg: Message):
    response = agent.get_response(msg.content)
    return Message(content=response, role="assistant", created_at=datetime.now(timezone.utc))

router.post("update-knowledge")
async def update_knowledge():
    pass