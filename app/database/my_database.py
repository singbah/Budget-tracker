# app/database/my_database.py
import os
import sys
import sqlite3

# -----FIND AND INIT DATABASE--- #

def get_db_path():
    """Resolve the SQLite database path, supporting both development and PyInstaller builds."""
    if getattr(sys, 'frozen', False):
        # Running as a compiled PyInstaller executable (stores DB next to the binary)
        base_dir = os.path.dirname(sys.executable)
    else:
        # Running as a standard script (navigates up from app/database/my_database.py to root)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        
    return os.path.join(base_dir, "app", "database", "budget_tracker_db.db")

def get_connection():
    """Open and return a SQLite database connection."""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    """Initialize database tables and default categories."""
    with get_connection() as conn:
        cur = conn.cursor()
        
        # Categories table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)
        
        # Transactions table with foreign key linkage
        cur.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                price REAL NOT NULL,
                necessity_level TEXT,
                impulse_type TEXT,
                spend_rating INTEGER NOT NULL DEFAULT 1,
                was_planned INTEGER DEFAULT 0,
                notes TEXT,
                date TEXT DEFAULT CURRENT_TIMESTAMP,
                category_id INTEGER,
                FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
            )
        """)
        
        # Insert default categories if none exist
        cur.execute("SELECT COUNT(*) FROM categories")
        if cur.fetchone()[0] == 0:
            default_cats = [("Food & Dining",), ("Transport",), ("Bills & Utilities",), ("Shopping",), ("Entertainment",)]
            cur.executemany("INSERT INTO categories (name) VALUES (?)", default_cats)
            
        conn.commit()

# --- CRUD OPERATIONS ---

def insert_transaction(item_name, price, necessity_level, impulse_type, spend_rating, was_planned, notes, category_id):
    """Insert a new transaction."""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO transactions (item_name, price, necessity_level, impulse_type, spend_rating, was_planned, notes, category_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (item_name, price, necessity_level, impulse_type, spend_rating, was_planned, notes, category_id))
        conn.commit()
        return cur.lastrowid

def get_all_transactions():
    """Fetch all transactions joined with their category names."""
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("""
            SELECT t.id, t.item_name, t.price, c.name AS category_name, t.necessity_level, 
                   t.spend_rating, t.was_planned, t.date, t.notes
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            ORDER BY t.date DESC
        """)
        rows =  cur.fetchall()
        return [dict(row) for row in rows]

def get_transaction_by_id(trans_id):
    """Fetch a single transaction record by its ID."""
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM transactions WHERE id = ?", (trans_id,))
        row = cur.fetchone()
        return dict(row) if row else None

def update_transaction(trans_id, item_name, price, necessity_level, impulse_type, spend_rating, was_planned, notes, category_id):
    """Update an existing transaction record in the database."""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE transactions 
            SET item_name = ?, price = ?, necessity_level = ?, impulse_type = ?, 
                spend_rating = ?, was_planned = ?, notes = ?, category_id = ?
            WHERE id = ?
        """, (item_name, price, necessity_level, impulse_type, spend_rating, was_planned, notes, category_id, trans_id))
        conn.commit()

def delete_transaction(trans_id):
    """Delete a transaction by ID."""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM transactions WHERE id = ?", (trans_id,))
        conn.commit()

def get_categories():
    """Fetch all categories for populating Tkinter dropdowns."""
    with get_connection() as conn:
        # conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        cur.execute("SELECT id, name FROM categories")
        rows = cur.fetchall()
        return rows

def get_current_month_total():
    """Fetch total spending for the current calendar month."""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT SUM(price) 
            FROM transactions 
            WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
        """)
        result = cur.fetchone()[0]
        return result if result is not None else 0.0

def get_category_breakdown():
    """Fetch total spending grouped by category for the current month."""
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("""
            SELECT c.name AS category_name, SUM(t.price) AS total
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE strftime('%Y-%m', t.date) = strftime('%Y-%m', 'now')
            GROUP BY c.id
        """)
        return [dict(row) for row in cur.fetchall()]

def get_impulse_breakdown():
    """Fetch spending totals and transaction counts grouped by impulse/intent type for the current month."""
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("""
            SELECT impulse_type, SUM(price) AS total, COUNT(*) AS count
            FROM transactions
            WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
            GROUP BY impulse_type
        """)
        return [dict(row) for row in cur.fetchall()]

def get_impulse_ratio():
    """Calculate the percentage of total monthly spend driven by unplanned/impulse purchases."""
    with get_connection() as conn:
        cur = conn.cursor()
        # Total spend this month
        cur.execute("SELECT SUM(price) FROM transactions WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')")
        total_res = cur.fetchone()[0]
        total = total_res if total_res is not None else 0.0
        
        if total == 0.0:
            return 0.0
            
        # Impulse/Unplanned spend this month
        cur.execute("SELECT SUM(price) FROM transactions WHERE was_planned = 0 AND strftime('%Y-%m', date) = strftime('%Y-%m', 'now')")
        impulse_res = cur.fetchone()[0]
        impulse_total = impulse_res if impulse_res is not None else 0.0
        
        return (impulse_total / total) * 100

def get_filtered_transactions(keyword=None, category_name=None, start_date=None, end_date=None):
    """Fetch transactions filtered by keyword, category, and date range."""
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        query = """
            SELECT t.id, t.item_name, t.price, t.necessity_level, 
                   t.impulse_type, t.spend_rating, t.was_planned, t.notes, t.date,
                   c.name AS category_name
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE 1=1
        """
        params = []
        
        if keyword:
            query += " AND (LOWER(t.item_name) LIKE ? OR LOWER(t.notes) LIKE ?)"
            params.extend([f"%{keyword}%", f"%{keyword}%"])
            
        if category_name and category_name != "All Categories":
            query += " AND c.name = ?"
            params.append(category_name)
            
        if start_date:
            query += " AND t.date >= ?"
            params.append(start_date)
            
        if end_date:
            query += " AND t.date <= ?"
            params.append(end_date)
            
        query += " ORDER BY t.date DESC, t.id DESC"
        
        cur.execute(query, params)
        return [dict(row) for row in cur.fetchall()]
