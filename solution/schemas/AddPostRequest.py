from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from methods.countries import find_country


class AddPostRequest(BaseModel):
    content: str = Field(max_length=1000)
    tags: List[str] = []