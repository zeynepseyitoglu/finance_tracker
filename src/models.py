from pydantic import BaseModel
from typing import Optional

class Category(BaseModel):
    name: str
    color: Optional[str] = None

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'name': 'Food',
                    'color': 'blue'
                }
            ]
        }
    }

class Transaction(BaseModel):
    id: int
    title: str
    amount: float
    type: str  # 'income' or 'expense'
    description: Optional[str] = None
    category: Optional[Category] = None

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': 1,
                    'title': 'Grocery shopping',
                    'amount': 150.75,
                    'type': 'expense',
                    'description': 'Bought groceries for the week',
                    'category': {
                        'name': 'Food',
                        'color': 'blue'
                    }
                },
                {
                    'id': 2,
                    'title': 'Salary',
                    'amount': 3000.00,
                    'type': 'income',
                    'description': 'Monthly salary',
                    'category': {
                        'name': 'Income',
                        'color': 'green'
                    }
                }
            ]
        }
    }