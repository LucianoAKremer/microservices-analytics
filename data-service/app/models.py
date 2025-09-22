from pydantic import BaseModel
from typing import Optional

class Category(BaseModel):
    id: Optional[int] = None
    name: str

class Expense(BaseModel):
    id: Optional[int] = None
    amount: float
    description: str
    date: str  # ISO format
    category_id: int
    user_id: Optional[int] = None
