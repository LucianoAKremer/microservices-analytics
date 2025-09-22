from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Optional
import psycopg2
import os
import pandas as pd
import json
import requests

router = APIRouter()

DB_PARAMS = dict(
    host=os.environ.get("DB_HOST", "localhost"),
    port=os.environ.get("DB_PORT", 5432),
    user=os.environ.get("DB_USER", "expenses_user"),
    password=os.environ.get("DB_PASSWORD", "expenses_pass"),
    dbname=os.environ.get("DB_NAME", "expenses_db"),
)

def get_db():
    conn = psycopg2.connect(**DB_PARAMS)
    try:
        yield conn
    finally:
        conn.close()

# Validación JWT real
async def verify_jwt(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token JWT faltante o inválido")
    token = authorization.split(" ")[1]
    auth_url = os.environ.get("AUTH_SERVICE_URL", "http://auth-service:8001") + "/api/verify"
    try:
        resp = requests.get(auth_url, headers={"Authorization": f"Bearer {token}"}, timeout=3)
        if resp.status_code == 200:
            return resp.json()["user"]["user_id"]
        else:
            raise HTTPException(status_code=401, detail="Token inválido")
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")

# Endpoint: Resumen general de gastos
@router.get("/stats/summary")
async def summary_stats(user_id: int = Depends(verify_jwt), db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("SELECT amount FROM expenses WHERE user_id = %s", (user_id,))
        rows = cur.fetchall()
    if not rows:
        return {"total": 0, "average": 0, "count": 0}
    df = pd.DataFrame(rows, columns=["amount"])
    return {
        "total": float(df["amount"].sum()),
        "average": float(df["amount"].mean()),
        "count": int(df["amount"].count())
    }

# Endpoint: Gastos agrupados por categoría
@router.get("/stats/by-category")
async def stats_by_category(user_id: int = Depends(verify_jwt), db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("""
            SELECT c.name, SUM(e.amount) as total
            FROM expenses e
            JOIN categories c ON e.category_id = c.id
            WHERE e.user_id = %s
            GROUP BY c.name
            ORDER BY total DESC
        """, (user_id,))
        rows = cur.fetchall()
    return [{"category": r[0], "total": float(r[1])} for r in rows]

# Endpoint: Gastos mensuales (tendencia)
@router.get("/stats/monthly")
async def stats_monthly(user_id: int = Depends(verify_jwt), db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("""
            SELECT DATE_TRUNC('month', date) as month, SUM(amount) as total
            FROM expenses
            WHERE user_id = %s
            GROUP BY month
            ORDER BY month
        """, (user_id,))
        rows = cur.fetchall()
    return [{"month": str(r[0])[:7], "total": float(r[1])} for r in rows]

# Endpoint: Top N gastos individuales
@router.get("/stats/top-expenses")
async def top_expenses(user_id: int = Depends(verify_jwt), db=Depends(get_db), n: int = 5):
    with db.cursor() as cur:
        cur.execute("""
            SELECT amount, description, date, category_id
            FROM expenses
            WHERE user_id = %s
            ORDER BY amount DESC
            LIMIT %s
        """, (user_id, n))
        rows = cur.fetchall()
    return [
        {"amount": float(r[0]), "description": r[1], "date": str(r[2]), "category_id": r[3]} for r in rows
    ]

# Endpoint: Template para gráfico de barras por categoría
@router.get("/chart/bar-category")
async def chart_bar_category(user_id: int = Depends(verify_jwt), db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("""
            SELECT c.name, SUM(e.amount) as total
            FROM expenses e
            JOIN categories c ON e.category_id = c.id
            WHERE e.user_id = %s
            GROUP BY c.name
            ORDER BY total DESC
        """, (user_id,))
        rows = cur.fetchall()
    labels = [r[0] for r in rows]
    data = [float(r[1]) for r in rows]
    return {
        "type": "bar",
        "data": {
            "labels": labels,
            "datasets": [{
                "label": "Gasto por categoría",
                "data": data,
                "backgroundColor": "#4e79a7"
            }]
        }
    }

# Endpoint: Template para gráfico de líneas mensual
@router.get("/chart/line-monthly")
async def chart_line_monthly(user_id: int = Depends(verify_jwt), db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("""
            SELECT DATE_TRUNC('month', date) as month, SUM(amount) as total
            FROM expenses
            WHERE user_id = %s
            GROUP BY month
            ORDER BY month
        """, (user_id,))
        rows = cur.fetchall()
    labels = [str(r[0])[:7] for r in rows]
    data = [float(r[1]) for r in rows]
    return {
        "type": "line",
        "data": {
            "labels": labels,
            "datasets": [{
                "label": "Gasto mensual",
                "data": data,
                "borderColor": "#f28e2b",
                "fill": False
            }]
        }
    }

# Endpoint: Template para gráfico de torta por categoría
@router.get("/chart/pie-category")
async def chart_pie_category(user_id: int = Depends(verify_jwt), db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("""
            SELECT c.name, SUM(e.amount) as total
            FROM expenses e
            JOIN categories c ON e.category_id = c.id
            WHERE e.user_id = %s
            GROUP BY c.name
            ORDER BY total DESC
        """, (user_id,))
        rows = cur.fetchall()
    labels = [r[0] for r in rows]
    data = [float(r[1]) for r in rows]
    return {
        "type": "pie",
        "data": {
            "labels": labels,
            "datasets": [{
                "label": "Distribución por categoría",
                "data": data,
                "backgroundColor": ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f", "#edc949"]
            }]
        }
    }
