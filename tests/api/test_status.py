import json
from fixture import test_client

def test_status_page(test_client):
    response = test_client.get('/api/')
    assert response.status_code == 200
    r_json = json.loads(response.data)
    assert 'description' in r_json
    assert r_json['version'] == '0.1.0'