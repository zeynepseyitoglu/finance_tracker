from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TransactionCreate(BaseModel):
    title: str
    amount: float
    type: str
    description: Optional[str] = None
    category: Optional[str] = None

class TransactionResponse(BaseModel):
    id: int
    title: str
    amount: float
    type: str
    description: Optional[str] = None
    category: Optional[str] = None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }