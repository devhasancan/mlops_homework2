import pytest
import json
from src.app import app

@pytest.fixture
def client():
    """Configures the Flask test client for integration testing."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test the liveness probe (health check) endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {"status": "ok"}

def test_prediction_endpoint(client):
    """
    Component Test: Verifies the full prediction pipeline 
    (feature engineering + inference) with valid input.
    """
    payload = {
        "neighborhood": "Kadikoy",
        "area": 120
    }
    
    response = client.post('/predict', 
                           data=json.dumps(payload),
                           content_type='application/json')
    
    # Check for HTTP 200 OK
    assert response.status_code == 200
    
    # Validate response structure
    data = response.json
    assert "estimated_price" in data
    assert "bucket_index" in data
    assert data["status"] == "success"

def test_prediction_error_handling(client):
    """Test API response for invalid or incomplete input data."""
    # Invalid payload: Negative area and missing 'neighborhood'
    payload = {"area": -50} 
    
    response = client.post('/predict', 
                           data=json.dumps(payload),
                           content_type='application/json')
                           
    assert response.status_code == 400