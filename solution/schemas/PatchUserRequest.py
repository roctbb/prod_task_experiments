from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from methods.countries import find_country


class PatchUserRequest(BaseModel):
    countryCode: Optional[str] = Field(max_length=2, pattern=r'[a-zA-Z]{2}', default=None)
    isPublic: Optional[bool] = None
    phone: Optional[str] = Field(max_length=20, pattern=r'\+[\d]+', default=None)
    image: Optional[str] = Field(max_length=200, default=None)

    @field_validator("countryCode")
    @classmethod
    def validate_countryCode(cls, value):
        try:
            country = find_country(value)
        except:
            raise ValueError('Country not found')

        return value
