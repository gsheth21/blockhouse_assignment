from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        Base.metadata.create_all(bind=engine)
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_order():
    response = client.post(
        "/orders",
        json={"symbol": "BTC", "price": 50000.0, "quantity": 1, "order_type": "BUY"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "BTC"

def test_read_orders():
    response = client.get("/orders")
    assert response.status_code == 200
    assert len(response.json()) >= 1