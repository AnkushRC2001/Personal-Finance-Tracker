import sqlite3

def clear_database():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    
    try:
        # Delete all rows from tables
        cursor.execute("DELETE FROM transactions")
        cursor.execute("DELETE FROM budgets")
        
        # Optional: Reset auto-increment counters
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='transactions'")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='budgets'")
        
        conn.commit()
        print("[SUCCESS] All records deleted successfully. Database is clean.")
        
    except Exception as e:
        print(f"[ERROR] Error clearing database: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    clear_database()
