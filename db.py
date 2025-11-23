import sqlite3
import pandas as pd

# Connect to DB (creates file if not exists)
conn = sqlite3.connect("finance.db", check_same_thread=False)
cursor = conn.cursor()

# Create transactions table
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    txn_date TEXT NOT NULL, -- ISO 8601 format (YYYY-MM-DD) preferred
    description TEXT,
    amount REAL NOT NULL,
    category TEXT
)
""")

# Create budgets table
cursor.execute("""
CREATE TABLE IF NOT EXISTS budgets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL UNIQUE,
    budget_limit REAL NOT NULL
)
""")

conn.commit()

# Insert transaction
def add_transaction(txn_date, description, amount, category):
    try:
        cursor.execute(
            "INSERT INTO transactions (txn_date, description, amount, category) VALUES (?, ?, ?, ?)",
            (txn_date, description, amount, category)
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database Error: {e}")
        # In a real app, we might want to raise this or log it properly

# Fetch all transactions as DataFrame
def get_transactions():
    return pd.read_sql_query("SELECT * FROM transactions", conn)

# Set or update budget
def set_budget(category, limit):
    cursor.execute("""
        INSERT OR REPLACE INTO budgets (id, category, budget_limit)
        VALUES ((SELECT id FROM budgets WHERE category = ?), ?, ?)
    """, (category, category, limit))
    conn.commit()

# Check budgets
def check_budgets():
    query = """
        SELECT b.category, b.budget_limit, IFNULL(SUM(t.amount), 0) as spent
        FROM budgets b
        LEFT JOIN transactions t ON b.category = t.category
        GROUP BY b.category
    """
    return pd.read_sql_query(query, conn)
