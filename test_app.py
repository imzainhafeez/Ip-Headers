import pytest
from app import app

@pytest.fixture
def client():
    # Set up the testing client
    with app.test_client() as client:
        yield client

def test_index_no_headers(client):
    # Test with no headers
    response = client.get('/test')
    data = response.get_json()

    # Check the default IP assignment to remote_addr
    assert data['client_ip']['value'] == '127.0.0.1'  # default client IP in Flask tests
    assert data['client_ip']['source'] == 'remote_addr'
    assert data['x_real_ip']['value'] is None
    assert data['x_forwarded_for']['value'] is None
    assert data['x_original_forwarded_for']['value'] is None

def test_index_with_client_ip_header(client):
    # Test with Client_IP header
    headers = {'Client_IP': '192.168.1.1'}
    response = client.get('/test', headers=headers)
    data = response.get_json()

    # Check if client IP is set correctly from Client_IP header
    assert data['client_ip']['value'] == '192.168.1.1'
    assert data['client_ip']['source'] == 'X-Forwarded-For'
    assert data['x_real_ip']['value'] is None

def test_index_with_x_real_ip_header(client):
    # Test with X-Real-IP header
    headers = {'X-Real-IP': '203.0.113.1'}
    response = client.get('/test', headers=headers)
    data = response.get_json()

    # Check if x_real_ip is set correctly from header
    assert data['x_real_ip']['value'] == '203.0.113.1'
    assert data['x_real_ip']['source'] == 'X-Real-IP header'

def test_index_with_all_headers(client):
    # Test with multiple headers
    headers = {
        'Client_IP': '192.168.1.1',
        'X-Real-IP': '203.0.113.1',
        'X-Forwarded-For': '198.51.100.1',
        'X-Original-Forwarded-For': '198.51.100.2'
    }
    response = client.get('/test', headers=headers)
    data = response.get_json()

    # Check values from all headers
    assert data['client_ip']['value'] == '192.168.1.1'
    assert data['client_ip']['source'] == 'X-Forwarded-For'
    assert data['x_real_ip']['value'] == '203.0.113.1'
    assert data['x_forwarded_for']['value'] == '198.51.100.1'
    assert data['x_original_forwarded_for']['value'] == '198.51.100.2'

