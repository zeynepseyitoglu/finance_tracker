from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from src.models import Transaction, TransactionResponse
from src.database import get_db
import src.crud as crud

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)

@router.get("", response_model=list[TransactionResponse], summary="Get All Transactions", description="Returns all transactions. Optionally filter by type — 'income' or 'expense'")
def get_transactions(transaction_type: str = None, db: Session = Depends(get_db)):
    return crud.get_transactions(db, transaction_type)

@router.get('/summary', summary="Get Transactions Summary", description="Returns a summary of total income, total expenses and net balance")
def get_summary(db: Session = Depends(get_db)):
    transactions = crud.get_transactions(db)
    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expenses = sum(t.amount for t in transactions if t.type == 'expense')
    net_balance = total_income - total_expenses
    return {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_balance': net_balance
    }

@router.get("/{transaction_id}", response_model=TransactionResponse, summary="Get Transaction", description="Returns a single transaction by its ID. Returns 404 if not found")
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = crud.get_transaction(db, transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction with id {transaction_id} not found"
        )
    return transaction

@router.post("", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED, summary="Create Transaction", description="Creates a new transaction. Requires title, amount and type")
def create_transaction(transaction: Transaction, db: Session = Depends(get_db)):
    return crud.create_transaction(
        db,
        title=transaction.title,
        amount=transaction.amount,
        type=transaction.type,
        description=transaction.description
    )

@router.put("/{transaction_id}", response_model=TransactionResponse, summary="Update Transaction", description="Completely replaces an existing transaction by ID. Returns 404 if not found")
def update_transaction(transaction_id: int, updated_transaction: Transaction, db: Session = Depends(get_db)):
    transaction = crud.update_transaction(
        db,
        transaction_id=transaction_id,
        title=updated_transaction.title,
        amount=updated_transaction.amount,
        type=updated_transaction.type,
        description=updated_transaction.description
    )
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction with id {transaction_id} not found"
        )
    return transaction

@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete Transaction", description="Deletes a transaction by ID. Returns 404 if not found")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = crud.delete_transaction(db, transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction with id {transaction_id} not found"
        )