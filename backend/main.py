from fastapi import FastAPI
from backend.routers.products import product_router
from backend.routers.requests import request_router
from backend.routers.auth import auth_router

app = FastAPI(title="Window site")
app.include_router(auth_router)
app.include_router(product_router)
app.include_router(request_router)