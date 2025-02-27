import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from app.main import app, get_session

TEST_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})

def override_get_session():
    with Session(test_engine) as session:
        yield session

app.dependency_overrides[get_session] = override_get_session

SQLModel.metadata.create_all(test_engine)

client = TestClient(app)

def test_create_order():
    response = client.post(
        "/orders/",
        json={"symbol": "BTC", "price": 50000.0, "quantity": 1, "order_type": "BUY"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "BTC"
    assert data["price"] == 50000.0
    assert data["quantity"] == 1
    assert data["order_type"] == "BUY"

def test_read_orders():
    response = client.get("/orders/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
