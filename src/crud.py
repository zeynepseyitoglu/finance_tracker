from sqlalchemy.orm import Session
from src.db_models import Transaction

def get_transactions(db: Session, transaction_type: str = None):
    if transaction_type:
        return db.query(Transaction).filter(Transaction.type == transaction_type).all()
    return db.query(Transaction).all()

def get_transaction(db: Session, transaction_id: int):
    return db.query(Transaction).filter(Transaction.id == transaction_id).first()

def create_transaction(db: Session, title: str, amount: float, type: str, description: str = None):
    transaction = Transaction(title=title, amount=amount, type=type, description=description)
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

def update_transaction(db: Session, transaction_id: int, title: str, amount: float, type: str, description: str = None):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if transaction:
        transaction.title = title
        transaction.amount = amount
        transaction.type = type
        transaction.description = description
        db.commit()
        db.refresh(transaction)
    return transaction

def delete_transaction(db: Session, transaction_id: int):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if transaction:
        db.delete(transaction)
        db.commit()
    return transaction