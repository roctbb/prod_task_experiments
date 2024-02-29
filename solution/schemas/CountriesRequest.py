from pydantic import BaseModel
from typing import List, Optional

class CountriesRequest(BaseModel):
    region: List[str] = []