import pytest
from flask import Flask
from app.app import app
from app.database import init_db, get_db_connection

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    # Setup: initialize the database
    init_db()
    yield
    # Teardown: clean up the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM processed_debts")
    conn.commit()
    conn.close()

@pytest.fixture
def clear_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM processed_debts")
    conn.commit()
    conn.close()
    yield
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM processed_debts")
    conn.commit()
    conn.close()
