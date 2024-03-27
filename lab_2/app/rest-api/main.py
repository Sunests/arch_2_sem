from fastapi import FastAPI
from routers.user_router import router as user_router
from init_files.data_init import PSQLManager
PSQLManager.init_database()
app = FastAPI()

app.include_router(user_router, tags=["users_tag"], prefix="/users")
