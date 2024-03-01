from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from methods.countries import find_country

class PaginationRequest(BaseModel):
    limit: Optional[int] = None
    offset: Optional[int] = None