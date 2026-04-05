from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import TransactionCreate, TransactionResponse
from src.async_database import get_db
import src.crud as crud

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)

@router.get("", response_model=list[TransactionResponse], summary="Get All Transactions", description="Returns all transactions. Optionally filter by type — 'income' or 'expense'")
async def get_transactions(transaction_type: str = None, db: AsyncSession = Depends(get_db)):
    return await crud.get_transactions(db, transaction_type)

@router.get('/summary', summary="Get Transactions Summary", description="Returns a summary of total income, total expenses and net balance")
async def get_summary(db: AsyncSession = Depends(get_db)):
    transactions = await crud.get_transactions(db)
    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expenses = sum(t.amount for t in transactions if t.type == 'expense')
    net_balance = total_income - total_expenses
    return {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_balance': net_balance
    }

@router.get("/{transaction_id}", response_model=TransactionResponse, summary="Get Transaction", description="Returns a single transaction by its ID. Returns 404 if not found")
async def get_transaction(transaction_id: int, db: AsyncSession = Depends(get_db)):
    transaction = await crud.get_transaction(db, transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction with id {transaction_id} not found"
        )
    return transaction

@router.post("", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED, summary="Create Transaction", description="Creates a new transaction. Requires title, amount and type")
async def create_transaction(transaction: TransactionCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_transaction(
        db,
        title=transaction.title,
        amount=transaction.amount,
        type=transaction.type,
        description=transaction.description,
        category=transaction.category
    )

@router.put("/{transaction_id}", response_model=TransactionResponse, summary="Update Transaction", description="Completely replaces an existing transaction by ID. Returns 404 if not found")
async def update_transaction(transaction_id: int, updated_transaction: TransactionCreate, db: AsyncSession = Depends(get_db)):
    transaction = await crud.update_transaction(
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
async def delete_transaction(transaction_id: int, db: AsyncSession = Depends(get_db)):
    transaction = await crud.delete_transaction(db, transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction with id {transaction_id} not found"
        )