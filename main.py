from fastapi import FastAPI, HTTPException, Request, status
from src.models import Transaction, TransactionResponse
from fastapi.responses import JSONResponse


app = FastAPI(
    title='Finance Tracker API',
    description='A simple API for tracking income and expenses',
    version='1.0.0'
)

transactions = []

@app.exception_handler(Exception)
async def global_exception_handler(request:Request, exc:Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            'error': 'Internal Server Error',
            'detail': 'Something went wrong on our end. Please try again later.'
        }
    )


@app.get('/', summary='Root', description='Check if the API is running', tags=['General'])
def root():
    return {'message': 'Finance tracker api is running!'}

@app.get('/health', summary='Health Check', description='Check the health status of the API', tags=['General'])
def health_check():
    return {'status': 'healthy', 'version': '1.0.0'}


@app.get('/transactions', response_model=list[Transaction], summary='Get Transactions', description='Retrieve a list of all transactions', tags=['Transactions'])
def get_transactions(transaction_type: str = None):
    # Placeholder for fetching transactions from a database
    if transaction_type:
        filtered = [t for t in transactions if t.type == transaction_type]
        return filtered
    return transactions

@app.get('/transactions/{transaction_id}', response_model=Transaction, summary='Get Transaction by ID', description='Retrieve a single transaction by its ID', tags=['Transactions'])
def get_transaction(transaction_id: int):
    for t in transactions:
        if t.id == transaction_id:
            return t
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='Transaction not found')
    
@app.post('/transactions', response_model=TransactionResponse, status_code=status.HTTP_201_CREATED, summary='Create Transaction', description='Create a new transaction', tags=['Transactions'])
def create_transaction(transaction: Transaction):
    transactions.append(transaction)
    return transaction

@app.put("/transactions/{transaction_id}", response_model=TransactionResponse, summary='Update Transaction', description='Update an existing transaction', tags=['Transactions'])
def update_transaction(transaction_id: int, updated_transaction: Transaction):
    for index, t in enumerate(transactions):
        if t.id == transaction_id:
            transactions[index] = updated_transaction
            return updated_transaction
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Transaction with id {transaction_id} not found"
    )

@app.delete("/transactions/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT, summary='Delete Transaction', description='Delete a transaction by its ID', tags=['Transactions'])
def delete_transaction(transaction_id: int):
    for index, t in enumerate(transactions):
        if t.id == transaction_id:
            transactions.pop(index)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"Transaction with id {transaction_id} not found")