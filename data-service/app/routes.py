from fastapi import APIRouter, HTTPException, Depends, Header
from typing import List, Optional
from app.models import Expense, Category

router = APIRouter()

# Simulación de almacenamiento en memoria
expenses_db = []
categories_db = [Category(id=1, name="General")]

# Middleware simulado de validación JWT
async def verify_jwt(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token JWT faltante o inválido")
    # Aquí se validaría el JWT real
    return 1  # user_id simulado

@router.post("/expenses", response_model=Expense)
async def create_expense(expense: Expense, user_id: int = Depends(verify_jwt)):
    expense.id = len(expenses_db) + 1
    expense.user_id = user_id
    expenses_db.append(expense)
    return expense

@router.get("/expenses", response_model=List[Expense])
async def list_expenses(user_id: int = Depends(verify_jwt)):
    return [e for e in expenses_db if e.user_id == user_id]

@router.post("/categories", response_model=Category)
async def create_category(category: Category, user_id: int = Depends(verify_jwt)):
    category.id = len(categories_db) + 1
    categories_db.append(category)
    return category

@router.get("/categories", response_model=List[Category])
async def list_categories(user_id: int = Depends(verify_jwt)):
    return categories_db

