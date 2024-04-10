from fastapi import FastAPI
from routers.router import router as conferences_router

app = FastAPI()

app.include_router(conferences_router, tags=["Conferences"], prefix="/api")
