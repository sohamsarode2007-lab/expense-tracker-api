# Expense Tracker API

A small FastAPI service that records expenses and produces monthly totals by category,
using hand-written SQL. Runs on SQLite locally and PostgreSQL in Docker.

    docker compose up --build
    python -m pytest -q
