from datetime import date

import pytest

from app.db import add_expense, create_schema, make_engine, monthly_totals


@pytest.fixture
def engine():
    engine = make_engine("sqlite:///:memory:")
    create_schema(engine)
    return engine


def test_add_expense_returns_new_id(engine):
    first = add_expense(engine, 1250, "food", date(2026, 10, 3), "lunch")
    second = add_expense(engine, 900, "travel", date(2026, 10, 4))
    assert second == first + 1


def test_monthly_totals_group_by_category(engine):
    add_expense(engine, 1000, "food", date(2026, 10, 1))
    add_expense(engine, 500, "food", date(2026, 10, 20))
    add_expense(engine, 3000, "rent", date(2026, 10, 2))
    add_expense(engine, 700, "food", date(2026, 11, 1))
    assert monthly_totals(engine, 2026, 10) == {"rent": 3000, "food": 1500}


def test_december_includes_the_last_day(engine):
    add_expense(engine, 400, "other", date(2026, 12, 31))
    assert monthly_totals(engine, 2026, 12) == {"other": 400}


def test_invalid_expenses_are_rejected(engine):
    with pytest.raises(ValueError):
        add_expense(engine, 0, "food", date(2026, 10, 1))
    with pytest.raises(ValueError):
        add_expense(engine, 100, "gadgets", date(2026, 10, 1))
