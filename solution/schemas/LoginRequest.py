from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from methods.countries import find_country


class LoginRequest(BaseModel):
    login: str = Field(max_length=30, pattern=r'[a-zA-Z0-9-]+')
    password: str = Field(min_length=6, max_length=100)