from fastapi.testclient import (
    TestClient
)

from main import (
    api
)

client = TestClient(api)

def test_upload_photo():
    with open('test_images/logo.jpg', 'rb') as file:
        response = client.post('/upload/photo', files={'files': file})

        print(response.status_code)
        print(response.json())

    assert response.status_code == 200
    assert 'message' in response.json()

test_upload_photo()
