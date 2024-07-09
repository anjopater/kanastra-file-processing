import sqlite3

def get_db_connection():
    conn = sqlite3.connect('app/processing.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS processed_debts (
        debtId TEXT PRIMARY KEY,
        name TEXT,
        governmentId TEXT,
        email TEXT,
        debtAmount REAL,
        debtDueDate TEXT
    )
    ''')
    conn.commit()
    conn.close()

def insert_debt(row):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT OR IGNORE INTO processed_debts (debtId, name, governmentId, email, debtAmount, debtDueDate)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (row['debtId'], row['name'], row['governmentId'], row['email'], row['debtAmount'], row['debtDueDate']))
    conn.commit()
    conn.close()

def debt_exists(debt_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(1) FROM processed_debts WHERE debtId = ?', (debt_id,))
    exists = cursor.fetchone()[0]
    conn.close()
    return exists > 0
