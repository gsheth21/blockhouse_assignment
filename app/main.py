from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from app.schemas import OrderCreate, Order
from app.database import get_db, SessionLocal
from app.models import Base, OrderDB
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    retries = 5
    while retries > 0:
        try:
            db = SessionLocal()
            Base.metadata.create_all(bind=db.get_bind())
            db.close()
            break
        except Exception as e:
            retries -= 1
            time.sleep(5)
            if retries == 0:
                raise RuntimeError("Failed to connect to database") from e

@app.get("/gym")
def get_gym():
    return {"message": "List of orders"}

@app.post("/orders", response_model=Order)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = OrderDB(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.get("/orders", response_model=list[Order])
def read_orders(db: Session = Depends(get_db)):
    return db.query(OrderDB).all()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass