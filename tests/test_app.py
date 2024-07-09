def test_upload_csv(client):
    data = {
        'file': (open('tests/test_files/sample.csv', 'rb'), 'sample.csv')
    }
    response = client.post('/upload-csv', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert 'job_id' in response.json

def test_get_status(client):
    response = client.get('/status/some_job_id')
    assert response.status_code == 404  # Assuming the job_id does not exist
    assert 'error' in response.json
