"""Unit tests for the 21st Agents SDK Flask application."""
import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, PRODUCT, API_VERSION


@pytest.fixture
def client():
    """Create a test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestHomePage:
    """Test home page routes."""

    def test_home_page(self, client):
        """Test that home page loads successfully."""
        response = client.get('/')
        assert response.status_code == 200

    def test_features_page(self, client):
        """Test that features page loads successfully."""
        response = client.get('/features')
        assert response.status_code == 200

    def test_about_page(self, client):
        """Test that about page loads successfully."""
        response = client.get('/about')
        assert response.status_code == 200


class TestAPIEndpoints:
    """Test API endpoints."""

    def test_get_product(self, client):
        """Test GET /api/product endpoint."""
        response = client.get('/api/product')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'data' in data
        assert data['data']['name'] == PRODUCT['name']

    def test_product_contains_required_fields(self, client):
        """Test that product API returns all required fields."""
        response = client.get('/api/product')
        data = response.get_json()
        product = data['data']

        required_fields = ['name', 'tagline', 'description', 'votes', 'comments', 'maker']
        for field in required_fields:
            assert field in product, f"Missing field: {field}"

    def test_vote_endpoint(self, client):
        """Test POST /api/vote endpoint."""
        response = client.post('/api/vote')
        assert response.status_code == 200
        data = response.get_json()
        assert 'success' in data
        assert 'votes' in data

    def test_vote_status(self, client):
        """Test GET /api/vote/status endpoint."""
        response = client.get('/api/vote/status')
        assert response.status_code == 200
        data = response.get_json()
        assert 'voted' in data
        assert 'votes' in data

    def test_get_comments(self, client):
        """Test GET /api/comments endpoint."""
        response = client.get('/api/comments')
        assert response.status_code == 200
        data = response.get_json()
        assert 'success' is True
        assert 'comments' in data

    def test_add_comment(self, client):
        """Test POST /api/comments endpoint."""
        response = client.post('/api/comments',
                               json={'name': 'Test User', 'content': 'Test comment'},
                               content_type='application/json')
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] is True

    def test_add_comment_without_name(self, client):
        """Test POST /api/comments without name."""
        response = client.post('/api/comments',
                               json={'content': 'Anonymous comment'},
                               content_type='application/json')
        assert response.status_code == 201
        data = response.get_json()
        assert data['comment']['name'] == 'Anonymous'

    def test_add_comment_without_content(self, client):
        """Test POST /api/comments without content should fail."""
        response = client.post('/api/comments',
                               json={'name': 'Test'},
                               content_type='application/json')
        assert response.status_code == 400


class TestHealthEndpoints:
    """Test health and stats endpoints."""

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get('/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'

    def test_stats_endpoint(self, client):
        """Test stats endpoint."""
        response = client.get('/stats')
        assert response.status_code == 200
        data = response.get_json()
        assert 'stats' in data


class TestErrorHandling:
    """Test error handlers."""

    def test_404_error(self, client):
        """Test 404 error handler."""
        response = client.get('/nonexistent')
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data


class TestAPIResponseFormat:
    """Test API response format."""

    def test_api_version_header(self, client):
        """Test that API version header is present."""
        response = client.get('/api/product')
        assert 'X-API-Version' in response.headers
        assert response.headers['X-API-Version'] == API_VERSION

    def test_content_type_header(self, client):
        """Test that content type header is present."""
        response = client.get('/api/product')
        assert 'Content-Type' in response.headers
