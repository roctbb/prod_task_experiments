from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from methods.countries import find_country


class FriendRequest(BaseModel):
    login: str = Field(max_length=30, pattern=r'[a-zA-Z0-9-]+')