import sys
import os
import sqlite3
from pprint import pprint
from tabulate import tabulate

# Ensure backend is on the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

# Connect to the database
DB_PATH = os.path.join(os.path.dirname(__file__), "library.db")
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row

def get_all_tables():
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    return [table['name'] for table in tables]

def show_table_contents(table_name):
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        if rows:
            # Convert SQLite rows to dictionaries
            data = [dict(row) for row in rows]
            # Use tabulate to format the output
            print(f"\n=== {table_name} ===")
            print(tabulate(data, headers="keys", tablefmt="grid"))
            print(f"Total rows: {len(rows)}")
        else:
            print(f"\n=== {table_name} ===")
            # Get column names
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [col['name'] for col in cursor.fetchall()]
            print(f"Columns: {', '.join(columns)}")
            print("No data in this table")
    except sqlite3.Error as e:
        print(f"Error querying table {table_name}: {e}")

def show_all_tables():
    tables = get_all_tables()
    print(f"Found {len(tables)} tables in the database:\n")
    for i, table in enumerate(tables, 1):
        print(f"{i}. {table}")
    
    print("\nShowing contents of all tables:")
    for table in tables:
        show_table_contents(table)

if __name__ == "__main__":
    print(f"Connected to database: {DB_PATH}\n")
    show_all_tables()
    conn.close() 