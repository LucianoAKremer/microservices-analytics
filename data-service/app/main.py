from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Data Service", description="CRUD de gastos y categorías", version="1.0.0")

app.include_router(router)

