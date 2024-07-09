import pandas as pd
import os
import logging
from app.services.boleto_generator_service import BoletoGeneratorService
from app.services.email_sender_service import EmailSenderService
from app.database import init_db, insert_debt, debt_exists
from app.validation import validate_row

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Log pandas version to ensure it's imported correctly
logger.debug(f"pandas version: {pd.__version__}")

boleto_generator = BoletoGeneratorService()
email_sender = EmailSenderService()

def process_chunk(chunk):
    processed_count = 0

    for index, row in chunk.iterrows():
        logger.debug(f"Processing row {index}: {row.to_dict()}")
        is_valid, message = validate_row(row)
        if not is_valid:
            logger.debug(f"Invalid row {index}: {message}")
            continue

        if not debt_exists(row['debtId']):
            logger.debug(f"Processing debt ID {row['debtId']} for row {index}")
            boleto_generator.generate_boleto(row)
            email_sender.send_email(row['email'], f"Your debt of {row['debtAmount']} is due on {row['debtDueDate']}")
            insert_debt(row)
            processed_count += 1
        else:
            logger.debug(f"Debt ID is already processed {row['debtId']} for row {index}")


    logger.debug(f"Processed {processed_count} rows in this chunk")
    return processed_count

def process_csv(file_path):
    try:
        logger.debug(f"Starting CSV processing for file: {file_path}")
        init_db()
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        logger.debug("Reading CSV in chunks")
        chunks = pd.read_csv(file_path, chunksize=10000)
        logger.debug("CSV read successfully")
        
        total_processed = 0
        for i, chunk in enumerate(chunks):
            logger.debug(f"Processing chunk {i}: {chunk.shape}")
            total_processed += process_chunk(chunk)
            logger.debug(f"Processed chunk {i}, total processed so far: {total_processed}")

        logger.debug(f"Completed CSV processing for file: {file_path}, total processed: {total_processed}")
        return {"total_processed": total_processed}
    except FileNotFoundError as e:
        logger.error(f"Error: {e}")
        return {"error": str(e)}
    except Exception as e:
        logger.error(f"Error processing CSV: {e}")
        return {"error": str(e)}
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.debug(f"Removed processed file: {file_path}")
