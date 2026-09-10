from fastapi import FastAPI
from backend.router import products


app = FastAPI(title="Window site")
app.include_router(products.router)