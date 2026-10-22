"""Data access for expenses, written with plain SQL on top of SQLAlchemy.

Locally the app uses SQLite; in Docker it connects to PostgreSQL through DATABASE_URL,
for example postgresql://expenses:expenses@db:5432/expenses.
"""
import os
from datetime import date

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

CATEGORIES = ("food", "travel", "rent", "utilities", "other")


def make_engine(url: str | None = None) -> Engine:
    return create_engine(url or os.getenv("DATABASE_URL", "sqlite:///./expenses.db"))


def create_schema(engine: Engine) -> None:
    with engine.begin() as conn:
        conn.execute(text(
            "CREATE TABLE IF NOT EXISTS expenses ("
            " id INTEGER PRIMARY KEY,"
            " amount_cents INTEGER NOT NULL CHECK (amount_cents > 0),"
            " category VARCHAR(20) NOT NULL,"
            " spent_on DATE NOT NULL,"
            " note VARCHAR(200) NOT NULL DEFAULT '')"
        ))


def add_expense(engine: Engine, amount_cents: int, category: str, spent_on: date, note: str = "") -> int:
    if amount_cents <= 0:
        raise ValueError("amount must be positive")
    if category not in CATEGORIES:
        raise ValueError(f"unknown category: {category}")
    with engine.begin() as conn:
        result = conn.execute(
            text("INSERT INTO expenses (amount_cents, category, spent_on, note) "
                 "VALUES (:amount, :category, :spent_on, :note) RETURNING id"),
            {"amount": amount_cents, "category": category, "spent_on": spent_on, "note": note},
        )
        return int(result.scalar_one())


def monthly_totals(engine: Engine, year: int, month: int) -> dict[str, int]:
    start = date(year, month, 1)
    end = date(year + (month == 12), month % 12 + 1, 1)
    with engine.connect() as conn:
        rows = conn.execute(
            text("SELECT category, SUM(amount_cents) AS total FROM expenses "
                 "WHERE spent_on >= :start AND spent_on < :end "
                 "GROUP BY category ORDER BY total DESC"),
            {"start": start, "end": end},
        )
        return {row.category: int(row.total) for row in rows}
