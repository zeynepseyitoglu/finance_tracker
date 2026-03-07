from pydantic import BaseModel
from typing import Optional

class Transaction(BaseModel):
    id: int
    title: str
    amount: float
    type: str  # 'income' or 'expense'
    description: Optional[str] = None