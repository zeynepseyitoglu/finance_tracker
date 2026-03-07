from fastapi import APIRouter, HTTPException, status
from src.models import Transaction, TransactionResponse

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)

transactions = []

@router.get("", response_model=list[Transaction], summary="Get All Transactions", description="Returns all transactions. Optionally filter by type — 'income' or 'expense'")
def get_transactions(transaction_type: str = None):
    if transaction_type:
        filtered = [t for t in transactions if t.type == transaction_type]
        return filtered
    return transactions

@router.get('/summary', summary="Get Transactions Summary", description="Returns a summary of total income, total expenses and net balance")
def get_summary():
    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expenses = sum(t.amount for t in transactions if t.type == 'expense')
    net_balance = total_income - total_expenses
    return {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_balance': net_balance
    }


@router.get("/{transaction_id}", response_model=Transaction, summary="Get Transaction", description="Returns a single transaction by its ID. Returns 404 if not found")
def get_transaction(transaction_id: int):
    for t in transactions:
        if t.id == transaction_id:
            return t
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Transaction with id {transaction_id} not found"
    )


@router.post("", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED, summary="Create Transaction", description="Creates a new transaction. Requires id, title, amount and type")
def create_transaction(transaction: Transaction):
    transactions.append(transaction)
    return transaction

@router.put("/{transaction_id}", response_model=Transaction, summary="Update Transaction", description="Completely replaces an existing transaction by ID. Returns 404 if not found")
def update_transaction(transaction_id: int, updated_transaction: Transaction):
    for index, t in enumerate(transactions):
        if t.id == transaction_id:
            transactions[index] = updated_transaction
            return updated_transaction
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Transaction with id {transaction_id} not found"
    )

@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete Transaction", description="Deletes a transaction by ID. Returns 404 if not found")
def delete_transaction(transaction_id: int):
    for index, t in enumerate(transactions):
        if t.id == transaction_id:
            transactions.pop(index)
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Transaction with id {transaction_id} not found"
    )