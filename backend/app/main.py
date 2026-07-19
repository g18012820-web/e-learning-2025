from fastapi import FastAPI
from app.api.v1 import api_router
from app.api.v1 import auth_v2
from app.api.v1 import media
from app.api.v1 import courses
from app.api.v1 import admin
from fastapi.responses import JSONResponse
from fastapi.requests import Request

app = FastAPI(title='E-Learning Backend API', version='0.3')

# include routers
app.include_router(api_router)
app.include_router(auth_v2.router)
app.include_router(media.router)
app.include_router(courses.router)
app.include_router(admin.router)

# global exception handler for JSON errors
@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"error": "internal_server_error", "message": str(exc)})

@app.get('/')
async def root():
    return {"message": "E-Learning Backend is running."}
