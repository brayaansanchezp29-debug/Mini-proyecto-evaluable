from fastapi import FastAPI
from app.routers import products
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Inventario v1")

app.include_router(products.router)