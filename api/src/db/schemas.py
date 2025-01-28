from typing import Any
from pydantic import BaseModel, ConfigDict, Field, Secret
from datetime import datetime, time, date as datetime_date
from uuid import UUID
from bson import ObjectId
from pydantic_core import core_schema



class PyObjectId(str):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: Any
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema(
                [
                    core_schema.is_instance_schema(ObjectId),
                    core_schema.chain_schema(
                        [
                            core_schema.str_schema(),
                            core_schema.no_info_plain_validator_function(cls.validate),
                        ]
                    ),
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )

    @classmethod
    def validate(cls, value) -> ObjectId:
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId")

        return ObjectId(value)
    

class Message(BaseModel):
    created_at :datetime 
    content :str
    role :str

class UserCreate(BaseModel):
    created_at :datetime 
    updated_at :datetime
    messages :list[Message] 

class UserCreateResponse(BaseModel):
    id : PyObjectId
    created_at :datetime
    updated_at :datetime
    messages :list[Message]

class UserResponse(BaseModel):
    id : PyObjectId
    created_at :datetime
    updated_at :datetime
    messages :list[Message]

class MessageUpdate(BaseModel):
    messages :list[Message]
