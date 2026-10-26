
import sqlite3
from datetime import date

DB_NAME = "expenses.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                expense_date TEXT NOT NULL
            )
        """)
        conn.commit()


def add_expense(title, amount, category, expense_date=None):
    if expense_date is None:
        expense_date = date.today().isoformat()

    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO expenses
            (title, amount, category, expense_date)
            VALUES (?, ?, ?, ?)
            """,
            (title, amount, category, expense_date)
        )
        conn.commit()


def get_expenses():
    with get_connection() as conn:
        cursor = conn.execute("""
            SELECT id, title, amount, category, expense_date
            FROM expenses
            ORDER BY expense_date DESC, id DESC
        """)
        return cursor.fetchall()


def delete_expense(expense_id):
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM expenses WHERE id = ?",
            (expense_id,)
        )
        conn.commit()
