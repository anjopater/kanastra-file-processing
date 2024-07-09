import re
from datetime import datetime
import pandas as pd


def validate_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_row(row):
    required_columns = ['name', 'governmentId', 'email', 'debtAmount', 'debtDueDate', 'debtId']
    
    for column in required_columns:
        if column not in row or pd.isnull(row[column]):
            return False, f"Missing or null value in required column: {column}"
    
    if not validate_email(row['email']):
        return False, f"Invalid email format: {row['email']}"
    
    if not validate_date(row['debtDueDate']):
        return False, f"Invalid date format: {row['debtDueDate']}"
    
    return True, "Valid row"
