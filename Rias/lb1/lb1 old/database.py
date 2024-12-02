import sqlite3

def create_connection():
    conn = sqlite3.connect("resources.db")
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            rank INTEGER,
            type TEXT,
            cost INTEGER,
            purchase_year INTEGER,
            profit INTEGER,
            expense INTEGER,
            start_year INTEGER,
            duration INTEGER,
            num_employees INTEGER,
            salary TEXT,
            deductions TEXT,
            material_expense INTEGER
        )
    """)
    conn.commit()
    conn.close()

def insert_resource(name, category, rank, type_, cost, purchase_year, profit, expense, 
                    start_year, duration, num_employees, salary, deductions, material_expense):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO resources (name, category, rank, type, cost, purchase_year, profit, expense, 
                               start_year, duration, num_employees, salary, deductions, material_expense)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, category, rank, type_, cost, purchase_year, profit, expense, start_year, 
          duration, num_employees, salary, deductions, material_expense))
    conn.commit()
    conn.close()

def fetch_resources():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM resources")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_resource(resource_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM resources WHERE id=?", (resource_id,))
    conn.commit()
    conn.close()
