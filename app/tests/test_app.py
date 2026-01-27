import pytest
import sys
import os

# Add the parent directory to sys.path to allow importing the app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_route(client):
    """Test that the home route returns a 200 status code."""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b"F5 AI Generated" in rv.data

def test_about_route(client):
    """Test that the about route returns a 200 status code."""
    rv = client.get('/about')
    assert rv.status_code == 200
    assert b"About" in rv.data

def test_docs_route(client):
    """Test that the docs route returns a 200 status code."""
    rv = client.get('/docs')
    assert rv.status_code == 200
    assert b"Educational Resources" in rv.data

def test_healthz_route(client):
    """Test that the health check route returns a 200 status code."""
    rv = client.get('/healthz')
    assert rv.status_code == 200
    assert rv.data == b"OK"

def test_alive_route(client):
    """Test that the alive route returns the content 'UP'."""
    rv = client.get('/alive')
    assert rv.status_code == 200
    assert b"UP" in rv.data

def test_404_error(client):
    """Test that a non-existent route returns a 404 status code."""
    rv = client.get('/non-existent-page')
    assert rv.status_code == 404
    assert b"Error 404: The Vibe is Lost" in rv.data

def test_api_status(client):
    """Test the /api/status endpoint."""
    rv = client.get('/api/status')
    assert rv.status_code == 200
    assert rv.headers['Content-Type'] == 'application/json'
    json_data = rv.get_json()
    assert json_data['status'] == 'active'
    assert json_data['version'] == 'v0.2'

def test_api_vibe_coding(client):
    """Test the /api/vibe-coding endpoint."""
    rv = client.get('/api/vibe-coding')
    assert rv.status_code == 200
    assert rv.headers['Content-Type'] == 'application/json'
    json_data = rv.get_json()
    assert 'topic' in json_data
    assert 'content' in json_data
    assert "Vibe coding" in json_data['content']

def test_api_ai_assisted_coding(client):
    """Test the /api/ai-assisted-coding endpoint."""
    rv = client.get('/api/ai-assisted-coding')
    assert rv.status_code == 200
    assert rv.headers['Content-Type'] == 'application/json'
    json_data = rv.get_json()
    assert 'topic' in json_data
    assert 'content' in json_data
    assert "ChatGPT" in json_data['content']

def test_openapi_spec_exists():
    """Test that the openapi/openapi.json file exists and is valid JSON."""
    path = os.path.join(os.path.dirname(__file__), '..', '..', 'openapi', 'openapi.json')
    assert os.path.exists(path)
    with open(path, 'r') as f:
        import json
        data = json.load(f)
        assert data['openapi'].startswith('3.0')
        assert 'paths' in data
        assert '/api/status' in data['paths']
        assert '/api/vibe-coding' in data['paths']
        assert '/api/ai-assisted-coding' in data['paths']

def test_login_get(client):
    """Test that GET /login returns 200."""
    rv = client.get('/login')
    assert rv.status_code == 200
    assert b"Sign in to your account" in rv.data

def test_login_post_success(client):
    """Test that POST /login succeeds with correct credentials."""
    rv = client.post('/login', data=dict(
        username='f5user',
        password='f5password'
    ), follow_redirects=True)
    assert rv.status_code == 200
    assert b"Welcome," in rv.data
    assert b"f5user" in rv.data

def test_login_post_failure(client):
    """Test that POST /login fails with incorrect credentials."""
    rv = client.post('/login', data=dict(
        username='wronguser',
        password='wrongpassword'
    ), follow_redirects=True)
    assert rv.status_code == 200 # Renders login page with error
    assert b"Invalid username or password" in rv.data

def test_contact_get(client):
    """Test that GET /contact returns 200."""
    rv = client.get('/contact')
    assert rv.status_code == 200
    assert b"Contact Us" in rv.data

def test_contact_post(client):
    """Test that POST /contact returns 200 and success message."""
    rv = client.post('/contact', data=dict(
        first_name='John',
        last_name='Doe',
        email='john.doe@example.com',
        message='Hello'
    ), follow_redirects=True)
    assert rv.status_code == 200
    assert b"Submission Received" in rv.data
    assert b"Thank you, John" in rv.data
