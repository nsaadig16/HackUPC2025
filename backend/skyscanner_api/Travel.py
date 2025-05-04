from typing import Optional
from pydantic import BaseModel
class Travel(BaseModel):
      id: Optional[int] = None
      username: str
      destination: Optional[list[str]] = []
      origin: str
      language: list[str]
      cabin_class: str
      disponibility: list[str]
      max_price: int
      hire_car: bool
      hotel: bool
      preferences: Optional[list[str]] = []