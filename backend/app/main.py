from fastapi import FastAPI
from app.api.v1 import router as api_router
from app.api.v1 import auth
from app.api.v1 import media

app = FastAPI(title='E-Learning Backend API', version='0.2')

app.include_router(api_router)
app.include_router(media.router)
app.include_router(auth.router)

@app.get('/')
async def root():
    return {"message": "E-Learning Backend is running."}
