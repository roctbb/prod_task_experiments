from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from methods.countries import find_country


class ChangePasswordRequest(BaseModel):
    oldPassword: str = Field(min_length=6, max_length=100)
    newPassword: str = Field(min_length=6, max_length=100)

    @field_validator("newPassword")
    @classmethod
    def validate_password(cls, value):
        if not (6 <= len(value) <= 100 and any(c.isupper() for c in value) and any(c.islower() for c in value) and any(
                c.isdigit() for c in value)):
            raise ValueError(
                'Password must contain at least one uppercase letter, one lowercase letter, one digit and be between 6 and 100 characters long')
        return value