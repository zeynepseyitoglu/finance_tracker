from fastapi import FastAPI, HTTPException, status
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='Transaction not found')
    
@app.post('/transactions', response_model=Transaction, status_code=status.HTTP_201_CREATED)
def create_transaction(transaction: Transaction):
    transactions.append(transaction)
    return transaction

@app.put("/transactions/{transaction_id}", response_model=Transaction)
def update_transaction(transaction_id: int, updated_transaction: Transaction):
    for index, t in enumerate(transactions):
        if t.id == transaction_id:
            transactions[index] = updated_transaction
            return updated_transaction
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Transaction with id {transaction_id} not found"
    )

@app.delete("/transactions/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(transaction_id: int):
    for index, t in enumerate(transactions):
        if t.id == transaction_id:
            del transactions[index]
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"Transaction with id {transaction_id} not found")