import time
import sys
import requests

# Configuration
WAIT_TIME = 5
MAX_RETRIES = 5
BASE_URL = "http://localhost:5000"

def wait_for_service():
    """Polls the /health endpoint to verify service availability (Liveness Probe)."""
    print(f"Checking service availability at {BASE_URL}...")
    
    for i in range(MAX_RETRIES):
        try:
            response = requests.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                print("SUCCESS: Health check passed. Service is ready.")
                return True
        except requests.exceptions.ConnectionError:
            print(f"Service not ready yet. Retrying in {WAIT_TIME}s ({i+1}/{MAX_RETRIES})...")
            time.sleep(WAIT_TIME)
            
    return False

def check_prediction():
    """Sends a sample inference request to verify model serving logic."""
    print("Sending sample prediction request...")
    payload = {"neighborhood": "Kadikoy", "area": 120}

    try:
        response = requests.post(f"{BASE_URL}/predict", json=payload)
        
        if response.status_code == 200:
            print("SUCCESS: Prediction endpoint responded correctly.")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"FAILURE: Unexpected status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"FAILURE: Request error: {e}")
        return False

if __name__ == "__main__":
    print("--- Starting Smoke Test ---")

    if not wait_for_service():
        print("CRITICAL: Service failed to start.")
        sys.exit(1) # Return non-zero exit code to fail the pipeline

    if not check_prediction():
        print("CRITICAL: Prediction test failed.")
        sys.exit(1) # Return non-zero exit code to fail the pipeline

    print("--- Smoke Test Passed Successfully ---")
    sys.exit(0)