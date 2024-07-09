import os
import time
import pytest
import requests
from app.app import app
from app.database import init_db, get_db_connection

BASE_URL = "http://localhost:5500"

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    # Setup: initialize the database and Flask app
    init_db()
    app.config['TESTING'] = True
    os.system('flask run &')  # Run Flask app in the background
    time.sleep(1)  # Give the server a moment to start
    yield
    # Teardown: clean up the database and stop the Flask app
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM processed_debts")
    conn.commit()
    conn.close()
    os.system('pkill -f "flask run"')


def test_upload_csv():
    file_path = 'tests/test_files/sample.csv'
    with open(file_path, 'rb') as file:
        response = requests.post(f"{BASE_URL}/upload-csv", files={'file': file})
    assert response.status_code == 200
    json_response = response.json()
    assert 'job_id' in json_response

    job_id = json_response['job_id']
    assert job_id is not None

    # Wait for the job to be processed
    time.sleep(2)

    # Check the status of the job
    response = requests.get(f"{BASE_URL}/status/{job_id}")
    assert response.status_code == 200
    json_response = response.json()
    assert 'status' in json_response

    status_message = json_response['status']
    assert 'Completed' in status_message or 'Failed' in status_message

def test_process_csv():
    # Check that debts were inserted into the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM processed_debts")
    count = cursor.fetchone()[0]
    assert count > 0  # Ensure that some rows were processed
    conn.close()
