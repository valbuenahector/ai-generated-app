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
    assert b"Welcome to the Vibe Coding Baseline" in rv.data

def test_about_route(client):
    """Test that the about route returns a 200 status code."""
    rv = client.get('/about')
    assert rv.status_code == 200
    assert b"About This Application" in rv.data

def test_docs_route(client):
    """Test that the docs route returns a 200 status code."""
    rv = client.get('/docs')
    assert rv.status_code == 200
    assert b"Educational Resources: Vibe Coding" in rv.data

def test_healthz_route(client):
    """Test that the health check route returns a 200 status code."""
    rv = client.get('/healthz')
    assert rv.status_code == 200
    assert rv.data == b"OK"

def test_404_error(client):
    """Test that a non-existent route returns a 404 status code."""
    rv = client.get('/non-existent-page')
    assert rv.status_code == 404
    assert b"Error 404: The Vibe is Lost" in rv.data
