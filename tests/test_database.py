from app.database import get_db_connection, init_db, insert_debt, debt_exists

def test_insert_debt(clear_db):
    row = {
        'debtId': '1234',
        'name': 'Test User',
        'governmentId': '5678',
        'email': 'test@example.com',
        'debtAmount': 100.0,
        'debtDueDate': '2024-12-31'
    }
    insert_debt(row)
    assert debt_exists('1234') is True

def test_no_duplicates(clear_db):
    row = {
        'debtId': '1234',
        'name': 'Test User',
        'governmentId': '5678',
        'email': 'test@example.com',
        'debtAmount': 100.0,
        'debtDueDate': '2024-12-31'
    }
    insert_debt(row)
    insert_debt(row)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM processed_debts WHERE debtId = '1234'")
    count = cursor.fetchone()[0]
    assert count == 1  # Ensure no duplicates
    conn.close()

def test_partial_processing(clear_db):
    row1 = {
        'debtId': '1235',
        'name': 'Test User 1',
        'governmentId': '5679',
        'email': 'test1@example.com',
        'debtAmount': 200.0,
        'debtDueDate': '2024-12-31'
    }
    row2 = {
        'debtId': '1236',
        'name': 'Test User 2',
        'governmentId': '5680',
        'email': 'test2@example.com',
        'debtAmount': 300.0,
        'debtDueDate': '2024-12-31'
    }
    insert_debt(row1)
    # Simulate partial processing by not inserting row2
    assert debt_exists('1235') is True
    assert debt_exists('1236') is False
