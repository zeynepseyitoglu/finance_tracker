from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def root():
    return {'message': 'Finance tracker api is running!'}