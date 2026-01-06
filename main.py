from fastmcp import FastMCP
import os
import tempfile
import sqlite3
import aiosqlite
from typing import Optional
import json

# -----------------------------
# PATH SETUP
# -----------------------------
TEMP_DIR = tempfile.gettempdir()
DB_PATH = os.path.join(TEMP_DIR, "expenses.db")
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")

print(f"Database path: {DB_PATH}")

# -----------------------------
# MCP INIT
# -----------------------------
mcp = FastMCP("ExpenseTracker")

# -----------------------------
# DB INITIALIZATION (SYNC)
# -----------------------------
def init_db():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    amount REAL NOT NULL,
                    category TEXT NOT NULL,
                    subcategory TEXT DEFAULT '',
                    note TEXT DEFAULT ''
                )
                """
            )
            # Write test
            conn.execute(
                "INSERT OR IGNORE INTO expenses(date, amount, category) VALUES ('2000-01-01', 0, 'test')"
            )
            conn.execute("DELETE FROM expenses WHERE category = 'test'")
            conn.commit()
            print("Database initialized successfully")
    except Exception as e:
        print(f"DB init error: {e}")
        raise

init_db()

# -----------------------------
# TOOLS
# -----------------------------

@mcp.tool()
async def add_expense(
    date: str,
    amount: float,
    category: str,
    subcategory: str = "",
    note: str = ""
) -> dict:
    """Add a new expense entry to the database."""
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            cur = await db.execute(
                """
                INSERT INTO expenses(date, amount, category, subcategory, note)
                VALUES (?, ?, ?, ?, ?)
                """,
                (date, amount, category, subcategory, note)
            )
            await db.commit()
            return {
                "status": "success",
                "id": cur.lastrowid,
                "message": "Expense added successfully"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@mcp.tool()
async def list_expenses(
    start_date: str,
    end_date: str
) -> list:
    """List expense entries within a date range."""
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            cur = await db.execute(
                """
                SELECT id, date, amount, category, subcategory, note
                FROM expenses
                WHERE date BETWEEN ? AND ?
                ORDER BY date DESC, id DESC
                """,
                (start_date, end_date)
            )
            cols = [c[0] for c in cur.description]
            rows = await cur.fetchall()
            return [dict(zip(cols, row)) for row in rows]
    except Exception as e:
        return [{"status": "error", "message": str(e)}]

@mcp.tool()
async def summarize(
    start_date: str,
    end_date: str,
    category: Optional[str] = None
) -> list:
    """Summarize expenses by category."""
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            query = """
                SELECT category, SUM(amount) AS total_amount, COUNT(*) AS count
                FROM expenses
                WHERE date BETWEEN ? AND ?
            """
            params = [start_date, end_date]

            if category:
                query += " AND category = ?"
                params.append(category)

            query += " GROUP BY category ORDER BY total_amount DESC"

            cur = await db.execute(query, params)
            cols = [c[0] for c in cur.description]
            rows = await cur.fetchall()
            return [dict(zip(cols, row)) for row in rows]
    except Exception as e:
        return [{"status": "error", "message": str(e)}]

# -----------------------------
# RESOURCE
# -----------------------------
@mcp.resource("expense:///categories", mime_type="application/json")
def categories() -> str:
    """Return expense categories."""
    default_categories = {
        "categories": [
            "Food & Dining",
            "Transportation",
            "Shopping",
            "Entertainment",
            "Bills & Utilities",
            "Healthcare",
            "Travel",
            "Education",
            "Business",
            "Other"
        ]
    }

    try:
        if os.path.exists(CATEGORIES_PATH):
            with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
                return f.read()
        return json.dumps(default_categories, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})
