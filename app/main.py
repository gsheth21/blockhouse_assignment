from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

class Order(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    symbol: str = Field(index=True)
    price: float = Field(index=True)
    quantity: int = Field(index=True)
    order_type: str = Field(index=True)

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
def createOrder(order: Order, session: SessionDep) -> Order:
    session.add(order)
    session.commit()
    session.refresh(order)
    return order

@app.get("/orders/")
def getOrder(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Order]:
    orders = session.exec(select(Order).offset(offset).limit(limit)).all()
    return orders