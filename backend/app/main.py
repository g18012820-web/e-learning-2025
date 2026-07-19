from fastapi import FastAPI
from app.api.v1 import router as api_router

app = FastAPI(title='E-Learning Backend API', version='0.1')

app.include_router(api_router)

@app.get('/')
async def root():
    return {"message": "E-Learning Backend is running."}
