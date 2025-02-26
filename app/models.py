from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class OrderDB(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    order_type = Column(String)