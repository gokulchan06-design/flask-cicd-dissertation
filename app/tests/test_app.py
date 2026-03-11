import pytest, json, sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app as flask_app

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'

def test_get_items(client):
    response = client.get('/items')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'items' in data
    assert data['count'] == 2

def test_compute_valid(client):
    response = client.post('/compute',
        data=json.dumps({'value': 5}),
        content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['result'] == 10

def test_compute_missing_value(client):
    response = client.post('/compute',
        data=json.dumps({}),
        content_type='application/json')
    assert response.status_code == 400
