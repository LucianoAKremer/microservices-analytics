from fastapi import APIRouter, HTTPException, Depends, Header, status, Path
from typing import List, Optional
from app.models import Expense, Category
import psycopg2
import os
import requests

router = APIRouter()

DB_PARAMS = dict(
    host=os.environ.get("DB_HOST", "localhost"),
    port=os.environ.get("DB_PORT", 5432),
    user=os.environ.get("DB_USER", "expenses_user"),
    password=os.environ.get("DB_PASSWORD", "expenses_pass"),
    dbname=os.environ.get("DB_NAME", "expenses_db"),
)

# Validación JWT real
async def verify_jwt(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token JWT faltante o inválido")
    token = authorization.split(" ")[1]
    # Corregido: endpoint correcto y puerto correcto
    auth_url = os.environ.get("AUTH_SERVICE_URL", "http://auth-service:8001") + "/api/verify"
    try:
        resp = requests.get(auth_url, headers={"Authorization": f"Bearer {token}"}, timeout=3)
        if resp.status_code == 200:
            # El endpoint /verify devuelve { valid: true, user: { user_id, ... } }
            return resp.json()["user"]["user_id"]
        else:
            raise HTTPException(status_code=401, detail="Token inválido")
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")

def get_db():
    conn = psycopg2.connect(**DB_PARAMS)
    try:
        yield conn
    finally:
        conn.close()

@router.post("/expenses", response_model=Expense, status_code=status.HTTP_201_CREATED)
async def create_expense(expense: Expense, user_id: int = Depends(verify_jwt), db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute(
            """
            INSERT INTO expenses (amount, description, date, category_id, user_id)
            VALUES (%s, %s, %s, %s, %s) RETURNING id
            """,
            (expense.amount, expense.description, expense.date, expense.category_id, user_id)
        )
        expense_id = cur.fetchone()[0]
        db.commit()
    return {**expense.dict(), "id": expense_id, "user_id": user_id}

@router.get("/expenses", response_model=List[Expense])
async def list_expenses(user_id: int = Depends(verify_jwt), db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("SELECT id, amount, description, date, category_id, user_id FROM expenses WHERE user_id = %s", (user_id,))
        rows = cur.fetchall()
    return [Expense(id=r[0], amount=float(r[1]), description=r[2], date=str(r[3]), category_id=r[4], user_id=r[5]) for r in rows]

@router.post("/categories", response_model=Category, status_code=status.HTTP_201_CREATED)
async def create_category(category: Category, user_id: int = Depends(verify_jwt), db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("INSERT INTO categories (name) VALUES (%s) RETURNING id", (category.name,))
        category_id = cur.fetchone()[0]
        db.commit()
    return {"id": category_id, "name": category.name}

@router.get("/categories", response_model=List[Category])
async def list_categories(user_id: int = Depends(verify_jwt), db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("SELECT id, name FROM categories")
        rows = cur.fetchall()
    return [Category(id=r[0], name=r[1]) for r in rows]

@router.delete("/expenses/{expense_id}", status_code=204)
async def delete_expense(expense_id: int = Path(...), user_id: int = Depends(verify_jwt), db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("DELETE FROM expenses WHERE id = %s AND user_id = %s", (expense_id, user_id))
        db.commit()
    return

@router.delete("/categories/{category_id}", status_code=204)
async def delete_category(category_id: int = Path(...), user_id: int = Depends(verify_jwt), db=Depends(get_db)):
    try:
        with db.cursor() as cur:
            cur.execute("DELETE FROM categories WHERE id = %s", (category_id,))
            db.commit()
    except psycopg2.errors.ForeignKeyViolation:
        raise HTTPException(status_code=409, detail="No se puede borrar la categoría: existen gastos asociados a ella.")
    return
