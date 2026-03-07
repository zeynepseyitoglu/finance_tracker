from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from routers import transactions

app = FastAPI(
    title='Finance Tracker API',
    description='A simple API for tracking income and expenses',
    version='1.0.0'
)


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


app.include_router(transactions.router)