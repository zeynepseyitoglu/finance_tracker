from pydantic import BaseModel
from typing import Optional

class Category(BaseModel):
    name: str
    color: Optional[str] = None

class Transaction(BaseModel):
    id: int
    title: str
    amount: float
    type: str  # 'income' or 'expense'
    description: Optional[str] = None
    category: Optional[Category] = None