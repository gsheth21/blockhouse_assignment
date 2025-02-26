from fastapi import FastAPI
from app.routers import orders
from app.websocket import manager

app = FastAPI()

app.include_router(orders.router)

@app.on_event("startup")
async def startup():
    await manager.connect()