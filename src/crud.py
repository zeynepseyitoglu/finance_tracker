from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.db_models import Transaction

async def get_transactions(db: AsyncSession, transaction_type: str = None):
    if transaction_type:
        result = await db.execute(select(Transaction).filter(Transaction.type == transaction_type))
    else:
        result = await db.execute(select(Transaction))
    return result.scalars().all()

async def get_transaction(db: AsyncSession, transaction_id: int):
    result = await db.execute(select(Transaction).filter(Transaction.id == transaction_id))
    return result.scalars().first()

async def create_transaction(db: AsyncSession, title: str, amount: float, type: str, description: str = None, category: str = None):
    transaction = Transaction(title=title, amount=amount, type=type, description=description, category=category)
    db.add(transaction)
    await db.commit()
    await db.refresh(transaction)
    return transaction

async def update_transaction(db: AsyncSession, transaction_id: int, title: str, amount: float, type: str, description: str = None, category: str = None):
    result = await db.execute(select(Transaction).filter(Transaction.id == transaction_id))
    transaction = result.scalars().first()
    if transaction:
        transaction.title = title
        transaction.amount = amount
        transaction.type = type
        transaction.description = description
        transaction.category = category
        await db.commit()
        await db.refresh(transaction)
    return transaction

async def delete_transaction(db: AsyncSession, transaction_id: int):
    result = await db.execute(select(Transaction).filter(Transaction.id == transaction_id))
    transaction = result.scalars().first()
    if transaction:
        await db.delete(transaction)
        await db.commit()
    return transaction