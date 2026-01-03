"""
Main application module for the House Price Prediction Service.
Exposes Flask endpoints for health checks and predictions.
"""
from flask import Flask, request, jsonify
from src.features import HousePricePreprocessor

app = Flask(__name__)
preprocessor = HousePricePreprocessor()

@app.route('/health', methods=['GET'])
def health_check():
    """Liveness probe for smoke testing."""
    return jsonify({"status": "ok"}), 200

@app.route('/predict', methods=['POST'])
def predict():
    """Inference endpoint. Applies feature engineering and returns prediction."""
    data = request.get_json()

    # Input validation
    if not data or 'area' not in data or 'neighborhood' not in data:
        return jsonify({"error": "Missing 'area' or 'neighborhood'."}), 400

    try:
        # Data quality check
        if not preprocessor.validate_area(data['area']):
            return jsonify({"error": "Invalid area (Outlier)."}), 400

        # Feature engineering (Hashing)
        bucket = preprocessor.hash_neighborhood(data['neighborhood'])

        # Simulated model inference
        estimated_price = (bucket * 1000) + (data['area'] * 500)

        return jsonify({
            "bucket_index": bucket,
            "estimated_price": estimated_price,
            "status": "success"
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    # Host 0.0.0.0 is required for Docker accessibility
    app.run(host='0.0.0.0', port=5000)