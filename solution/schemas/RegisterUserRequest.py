from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from methods.countries import find_country


class RegisterUserRequest(BaseModel):
    login: str = Field(max_length=30, pattern=r'[a-zA-Z0-9-]+')
    email: str = Field(max_length=50)
    password: str = Field(..., min_length=6, max_length=100)
    countryCode: str = Field(max_length=2, pattern=r'[a-zA-Z]{2}')
    isPublic: bool
    phone: Optional[str] = Field(max_length=20, pattern=r'\+[\d]+', default=None)
    image: str = Field(max_length=200, default=None)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if not (6 <= len(value) <= 100 and any(c.isupper() for c in value) and any(c.islower() for c in value) and any(
                c.isdigit() for c in value)):
            raise ValueError(
                'Password must contain at least one uppercase letter, one lowercase letter, one digit and be between 6 and 100 characters long')
        return value

    @field_validator("countryCode")
    @classmethod
    def validate_countryCode(cls, value):
        try:
            country = find_country(value)
        except:
            raise ValueError('Country not found')

        return value