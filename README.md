# Kanastra File Processing

This repository contains the Kanastra basic file processing service. Below you'll find instructions on how to deploy and test the service using Docker Compose.


## Installation

Clone the repository:

```bash
git clone https://github.com/anjopater/kanastra-file-processing.git
cd kanastra-file-processing
```

## Deployment
1. Using Docker Compose
2. Ensure you have Docker and Docker Compose installed.
3. Build and deploy the Docker image:
`docker-compose up`

Now you will be able to acces to the API.

## Run the unit testing
1. Execute the command `docker-compose exec api pytest`

## Run integration tests
1. Execute the command `docker-compose exec api pytest tests/integration_test.py`
if you have any issue, check the name of the service with `docker-compose ps` in the service column

### Test the real service

As this is a large file, the processing is done asynchronously. Doing it synchronously won't scale and will eventually block the main application process.

1. Make a request to the `/upload-csv` endpoint:
`curl -X POST http://localhost:5001/upload-csv -F "file=@path/to/your/file.csv"`

This will start the processing and return a job ID:
````
{
    "job_id": "3c836ebe-d84a-4cb2-a23a-f1b45a70e00f",
    "message": "CSV processing started"
}
````

2. Make a request to the /status/<job_id> endpoint:

 `curl http://localhost:5001/status/3c836ebe-d84a-4cb2-a23a-f1b45a70e00f`

````
{
    "status": "Processing"
}
````

This will return the status of the job:


NOTE: This is a very basic API, so you might find several points for improvement
