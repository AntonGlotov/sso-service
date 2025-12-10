import uvicorn
from fastapi import FastAPI
from config import settings
from endpoints import api_router
from logger import setup_logging


setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None
)
app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)