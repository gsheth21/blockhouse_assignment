from enum import Enum
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Field, Session, SQLModel, create_engine, select

class OrderType(str, Enum):
    BUY = "buy"
    SELL = "sell"

class Order(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    symbol: str = Field(index=True, min_length=1, max_length=10)
    price: float = Field(index=True, gt=0)
    quantity: int = Field(index=True, gt=0)
    order_type: OrderType = Field(index=True)

sqlite_file_name = "prod.db"
sqlite_url = f"sqlite:///./{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/orders/")
def create_order(order: Order, session: SessionDep) -> Order:
    session.add(order)
    try:
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Error saving order to the database")
    session.refresh(order)
    return order

@app.get("/orders/")
def get_orders(
    session: SessionDep,
    offset: Annotated[int, Query(ge=0)] = 0,  # Ensure non-negative offset
    limit: Annotated[int, Query(ge=0, le=100)] = 100,  # Limit between 0 and 100
) -> list[Order]:
    try:
        orders = session.exec(select(Order).offset(offset).limit(limit)).all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Error retrieving orders from the database")
    return orders