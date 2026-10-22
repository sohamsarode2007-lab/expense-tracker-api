from datetime import date

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.db import add_expense, create_schema, make_engine, monthly_totals

app = FastAPI(title="Expense Tracker API")
engine = make_engine()
create_schema(engine)


class ExpenseIn(BaseModel):
    amount_cents: int = Field(gt=0)
    category: str
    spent_on: date
    note: str = Field(default="", max_length=200)


@app.post("/expenses", status_code=201)
def create_expense(expense: ExpenseIn) -> dict[str, int]:
    try:
        expense_id = add_expense(engine, expense.amount_cents, expense.category, expense.spent_on, expense.note)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {"id": expense_id}


@app.get("/reports/{year}/{month}")
def monthly_report(year: int, month: int) -> dict[str, int]:
    if not 1 <= month <= 12:
        raise HTTPException(status_code=422, detail="month must be 1-12")
    return monthly_totals(engine, year, month)
