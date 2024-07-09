import pandas as pd
from app.process_csv import process_chunk, process_csv
from app.database import init_db, insert_debt, get_db_connection

def setup_module(module):
    # Initialize the database for testing
    init_db()

def teardown_module(module):
    # Clean up the database after tests
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM processed_debts")
    conn.commit()
    conn.close()

def test_process_large_csv(clear_db):
    large_chunk = pd.DataFrame([{
        'debtId': f'{i}',
        'name': f'Test User {i}',
        'governmentId': f'{1000 + i}',
        'email': f'test{i}@example.com',
        'debtAmount': '100.0',
        'debtDueDate': '2024-12-31'
    } for i in range(10000)])
    result = process_chunk(large_chunk)
    assert result == 10000  # All rows should be processed

def test_process_csv(clear_db):
    chunk = pd.DataFrame([
        {'debtId': '1236', 'name': 'Test User 3', 'governmentId': '5680', 'email': 'test3@example.com', 'debtAmount': '100.0', 'debtDueDate': '2024-12-31'},
        {'debtId': '1237', 'name': 'Test User 4', 'governmentId': '5681', 'email': 'test4@example.com', 'debtAmount': '100.0', 'debtDueDate': '2024-12-31'}
    ])
    result = process_chunk(chunk)
    assert result == 2  # All rows should be processed
