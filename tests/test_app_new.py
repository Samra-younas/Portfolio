import pytest
import json
from unittest.mock import patch, MagicMock
import anthropic
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import create_app, anthropic_service

@pytest.fixture
def app():
    """Create a test Flask app."""
    app = create_app('testing')
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()

@pytest.fixture
def mock_anthropic_service():
    """Mock the Anthropic service."""
    with patch('app.anthropic_service') as mock_service:
        yield mock_service

class TestHealthEndpoint:
    """Test cases for the /health endpoint."""
    
    def test_health_endpoint_success(self, client, mock_anthropic_service):
        """Test that /health returns 200 and correct status."""
        mock_anthropic_service.health_check.return_value = True
        
        response = client.get('/health')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'ok'
        assert data['anthropic_service'] == 'healthy'

class TestChatEndpoint:
    """Test cases for the /api/chat endpoint."""
    
    def test_chat_endpoint_success(self, client, mock_anthropic_service):
        """Test successful chat request with valid data."""
        mock_anthropic_service.chat.return_value = "Hello! I'm Samra Younas..."
        
        test_data = {
            "messages": [
                {"role": "user", "content": "Tell me about yourself"}
            ]
        }
        
        response = client.post('/api/chat', 
                              data=json.dumps(test_data),
                              content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'reply' in data
        assert data['reply'] == "Hello! I'm Samra Younas..."
    
    def test_chat_endpoint_no_messages(self, client):
        """Test chat endpoint with no messages provided."""
        test_data = {}
        
        response = client.post('/api/chat',
                              data=json.dumps(test_data),
                              content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

class TestStaticRoutes:
    """Test cases for static file serving."""
    
    def test_index_route(self, client):
        """Test serving the main index page."""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_chatbot_route(self, client):
        """Test serving the chatbot page."""
        response = client.get('/chatbot')
        assert response.status_code == 200

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
