-- PostgreSQL schema for the expense tracker (the app creates the same table on startup).
CREATE TABLE IF NOT EXISTS expenses (
    id SERIAL PRIMARY KEY,
    amount_cents INTEGER NOT NULL CHECK (amount_cents > 0),
    category VARCHAR(20) NOT NULL,
    spent_on DATE NOT NULL,
    note VARCHAR(200) NOT NULL DEFAULT ''
);

CREATE INDEX IF NOT EXISTS idx_expenses_spent_on ON expenses (spent_on);
