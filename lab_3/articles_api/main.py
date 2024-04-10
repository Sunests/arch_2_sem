from fastapi import FastAPI
from routers.router import router as articles_router

app = FastAPI()

app.include_router(articles_router, tags=["Articles"], prefix="/api")
