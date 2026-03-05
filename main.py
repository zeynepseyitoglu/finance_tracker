from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def root():
    return {'message': 'Finance tracker api is running!'}

@app.get('/health')
def health_check():
    return {'status': 'healthy', 'version': '1.0.0'}


@app.get('/transactions')
def get_transactions(transaction_type: str = None):
    # Placeholder for fetching transactions from a database
    transactions = [
        {'transaction_id': 1, 'amount': 100.0, 'currency': 'USD', 'type': 'income'},
        {'transaction_id': 2, 'amount': 50.0, 'currency': 'USD', 'type': 'expense'},
        {'transaction_id': 3, 'amount': 200.0, 'currency': 'USD', 'type': 'income'},
    ]
    
    if transaction_type:
        transactions = [t for t in transactions if t['type'] == transaction_type]
    
    return transactions

@app.get('/transactions/{transaction_id}')
def get_transaction(transaction_id: int):
    # Placeholder for fetching transaction details from a database
    return {
        'transaction_id': transaction_id,
        'amount': 100.0,
        'currency': 'USD',
        'description': 'Sample transaction'
    }
