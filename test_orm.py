from src.database import Base, engine, SessionLocal
from src.db_models import Transaction

Base.metadata.create_all(bind=engine)

db = SessionLocal()

# ─────────────────────────────────────────
# CLEAN SLATE
# ─────────────────────────────────────────
db.query(Transaction).delete()
db.commit()
print("Table cleared")

# ─────────────────────────────────────────
# CREATE
# ─────────────────────────────────────────
transaction1 = Transaction(title="Salary", amount=3000.00, type="income", description="Monthly salary")
transaction2 = Transaction(title="Rent", amount=800.00, type="expense", description="Monthly rent")
transaction3 = Transaction(title="Groceries", amount=150.00, type="expense", description="Weekly groceries")

db.add(transaction1)
db.add(transaction2)
db.add(transaction3)
db.commit()
print("\n--- AFTER CREATE ---")
results = db.query(Transaction).all()
for t in results:
    print(f"ID: {t.id} | Title: {t.title} | Amount: {t.amount} | Type: {t.type}")

# ─────────────────────────────────────────
# READ - get all
# ─────────────────────────────────────────
print("\n--- READ ALL ---")
all_transactions = db.query(Transaction).all()
for t in all_transactions:
    print(f"ID: {t.id} | Title: {t.title} | Amount: {t.amount} | Type: {t.type}")

# ─────────────────────────────────────────
# READ - get one by id
# ─────────────────────────────────────────
print("\n--- READ ONE ---")
single = db.query(Transaction).filter(Transaction.id == transaction1.id).first()
print(f"Found: {single.title} | Amount: {single.amount}")

# ─────────────────────────────────────────
# READ - filter by type
# ─────────────────────────────────────────
print("\n--- READ FILTERED ---")
expenses = db.query(Transaction).filter(Transaction.type == "expense").all()
for t in expenses:
    print(f"Expense: {t.title} | Amount: {t.amount}")

# ─────────────────────────────────────────
# UPDATE
# ─────────────────────────────────────────
print("\n--- AFTER UPDATE ---")
transaction_to_update = db.query(Transaction).filter(Transaction.id == transaction1.id).first()
transaction_to_update.amount = 3500.00
db.commit()
db.refresh(transaction_to_update)
print(f"Updated {transaction_to_update.title} amount to: {transaction_to_update.amount}")

# ─────────────────────────────────────────
# DELETE
# ─────────────────────────────────────────
print("\n--- AFTER DELETE ---")
transaction_to_delete = db.query(Transaction).filter(Transaction.id == transaction3.id).first()
db.delete(transaction_to_delete)
db.commit()
results = db.query(Transaction).all()
for t in results:
    print(f"ID: {t.id} | Title: {t.title} | Amount: {t.amount} | Type: {t.type}")

db.close()
print("\nDone!")