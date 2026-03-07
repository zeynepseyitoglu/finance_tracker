# Personal Finance Tracker API

A REST API built with FastAPI for tracking personal income and expenses. Supports full CRUD operations, transaction filtering, and financial summaries.

---

## Tech Stack

- **Python 3.12**
- **FastAPI** — web framework
- **Pydantic** — data validation
- **Uvicorn** — ASGI server

---

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/zeynepseyitoglu/finance_tracker.git
   cd finance_tracker
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv env
   env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## How to Run

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

Interactive docs available at `http://127.0.0.1:8000/docs`

---

## API Endpoints

| Method | Endpoint | Description | Status Code |
|--------|----------|-------------|-------------|
| GET | `/` | Check if API is running | 200 |
| GET | `/health` | Health check | 200 |
| GET | `/transactions` | Get all transactions | 200 |
| GET | `/transactions?transaction_type=income` | Filter by type | 200 |
| GET | `/transactions/{id}` | Get transaction by ID | 200 |
| POST | `/transactions` | Create a new transaction | 201 |
| PUT | `/transactions/{id}` | Update a transaction | 200 |
| DELETE | `/transactions/{id}` | Delete a transaction | 204 |
| GET | `/transactions/summary` | Get financial summary | 200 |

---

## Example Requests & Responses

### Create a Transaction
**POST** `/transactions`

Request body:
```json
{
  "id": 1,
  "title": "Monthly Salary",
  "amount": 3000.00,
  "type": "income",
  "description": "Salary for March",
  "category": {
    "name": "Work",
    "color": "blue"
  }
}
```

Response `201 Created`:
```json
{
  "id": 1,
  "title": "Monthly Salary",
  "amount": 3000.00,
  "type": "income"
}
```

---

### Get All Transactions
**GET** `/transactions`

Response `200 OK`:
```json
[
  {
    "id": 1,
    "title": "Monthly Salary",
    "amount": 3000.00,
    "type": "income",
    "description": "Salary for March"
  },
  {
    "id": 2,
    "title": "Groceries",
    "amount": 50.00,
    "type": "expense",
    "description": null
  }
]
```

---

### Get Financial Summary
**GET** `/transactions/summary`

Response `200 OK`:
```json
{
  "total_income": 3000.00,
  "total_expenses": 50.00,
  "net_balance": 2950.00
}
```

---

### Error Response Example
**GET** `/transactions/999`

Response `404 Not Found`:
```json
{
  "detail": "Transaction with id 999 not found"
}
```

---

## Project Structure

```
finance_tracker/
├── src/
│   ├── __init__.py
│   └── models.py
├── routers/
│   ├── __init__.py
│   └── transactions.py
├── main.py
├── requirements.txt
└── .gitignore
```

