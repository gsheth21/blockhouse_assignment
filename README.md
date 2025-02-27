# Blockhouse Assignment

## Overview
A REST API for managing trade orders, deployed on AWS EC2 with CI/CD via GitHub Actions. It supports order submission, retrieval.
Visit at: http://ec2-3-144-1-48.us-east-2.compute.amazonaws.com:8000/orders

## Features

### REST APIs
- **POST /orders:** Submit new trade orders (symbol, price, quantity, order_type).
- **GET /orders:** Retrieve all submitted orders.

### Database
- Uses SQLite for persistent storage.

### Containerized
- Dockerized application with Docker Compose for local development.

### CI/CD
- Automated testing and deployment via GitHub Actions.

## Tech Stack
- **Backend:** Python/FastAPI
- **Database:** SQLite
- **Containerization:** Docker, Docker Compose
- **Infrastructure:** AWS EC2 (Ubuntu)
- **CI/CD:** GitHub Actions
- **API Docs:** Swagger/OpenAPI

## Installation

### Prerequisites
- Docker & Docker Compose
- Python 3.9
- Packages listed in requirements.txt
```bash
pip install -r requirements.txt
```

### Local Setup
Clone the repository:
```bash
git clone https://github.com/gsheth21/blockhouse_assignment
cd blockhouse_assignment
```

Start the services with Docker Compose:

```bash
docker-compose up -d
```

Access the API at http://localhost:8000.

## API Documentation
Swagger UI: Access at http://ec2-3-144-1-48.us-east-2.compute.amazonaws.com:8000/docs after deployment.
Example POST /orders request:
```json
{
  "symbol": "BTC-USD",
  "price": 50000.0,
  "quantity": 0.5,
  "order_type": "buy"
}
```

## Deployment on AWS EC2
### EC2 Setup
Launched an Ubuntu EC2 instance (t2.micro).
Opened ports: 8000 (API), 22 (SSH), 5432 (SQLite).
Installed Docker & Docker Compose on EC2.
Running the Application
Deploy using:

```bash
docker-compose docker-compose.yml up -d
```

## CI/CD Pipeline
### GitHub Actions Workflow:
Tests are run on pull requests.

On merging to main, the Docker image is built, pushed to dockerhub and deployed via SSH.

Pre-built Image: gauravsheth01/orders-api:latest

Secrets used: DOCKERHUB_USERNAME, DOCKERHUB_TOKEN, EC2_HOST, EC2_SSH_KEY

## Testing
Run tests with:

```bash
pytest tests/
```