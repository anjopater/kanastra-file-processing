from flask import Flask, request, jsonify
import os
import uuid
import concurrent.futures
from app.process_csv import process_csv
from app.utils import compute_file_hash
from app.database import init_db, debt_exists, insert_debt
import logging
import pandas as pd

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
UPLOAD_FOLDER = 'app/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
init_db()

# Dictionary to store job statuses
job_status = {}

@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        logger.debug("No file part in request")
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        logger.debug("No selected file")
        return "No selected file", 400
    if file:
        temp_file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        logger.debug(f"Saving file to {temp_file_path}")
        file.save(temp_file_path)
        
        if os.path.exists(temp_file_path):
            logger.debug(f"File {temp_file_path} saved successfully")
        else:
            logger.error(f"File {temp_file_path} not found after save")
            return "File not found after save", 500
        
        file_hash = compute_file_hash(temp_file_path)
        file_path = os.path.join(UPLOAD_FOLDER, f"{file_hash}.csv")
        
        if not os.path.exists(file_path):
            os.rename(temp_file_path, file_path)
            logger.debug(f"File saved and renamed to: {file_path}")
        else:
            os.remove(temp_file_path)
            logger.debug(f"Duplicate file detected and removed: {temp_file_path}")

        # Generate a unique job ID
        job_id = str(uuid.uuid4())
        job_status[job_id] = "Processing"

        # Start the background job
        executor = concurrent.futures.ThreadPoolExecutor()
        executor.submit(process_csv_async, file_path, job_id)

        return jsonify({"message": "CSV processing started", "job_id": job_id})

def process_csv_async(file_path, job_id):
    try:
        result = process_csv(file_path)
        job_status[job_id] = f"Completed: {result['total_processed']} records processed"
    except Exception as e:
        job_status[job_id] = f"Failed: {str(e)}"
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.debug(f"Removed processed file: {file_path}")

@app.route('/status/<job_id>', methods=['GET'])
def get_status(job_id):
    if job_id in job_status:
        return jsonify({"status": job_status[job_id]})
    else:
        return jsonify({"error": "Job ID not found"}), 404

if __name__ == '__main__':
    logger.debug("Starting Flask app")
    app.run(host='0.0.0.0', port=5500)
