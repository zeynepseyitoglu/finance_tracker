from fastapi import FastAPI
from src.models import Transaction


app = FastAPI()

transactions = []


@app.get('/')
def root():
    return {'message': 'Finance tracker api is running!'}

@app.get('/health')
def health_check():
    return {'status': 'healthy', 'version': '1.0.0'}


@app.get('/transactions', response_model=list[Transaction])
def get_transactions(transaction_type: str = None):
    # Placeholder for fetching transactions from a database
    if transaction_type:
        filtered = [t for t in transactions if t.type == transaction_type]
        return filtered
    return transactions

@app.get('/transactions/{transaction_id}', response_model=Transaction)
def get_transaction(transaction_id: int):
    for t in transactions:
        if t.id == transaction_id:
            return t
        return {'error': 'Transaction not found'}
    
@app.post('/transactions', response_model=Transaction)
def create_transaction(transaction: Transaction):
    transactions.append(transaction)
    return transaction