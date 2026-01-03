import pytest
from src.features import HousePricePreprocessor

@pytest.fixture
def preprocessor():
    """Fixture to provide a fresh instance for each test."""
    return HousePricePreprocessor(num_buckets=100)

def test_validate_area_positive(preprocessor):
    """Test happy path for valid area input."""
    assert preprocessor.validate_area(120) is True

def test_validate_area_negative(preprocessor):
    """Test error handling for non-positive area values."""
    with pytest.raises(ValueError):
        preprocessor.validate_area(-50)
        
    with pytest.raises(ValueError):
        preprocessor.validate_area(0)

def test_validate_area_outlier(preprocessor):
    """Test boundary condition for outliers (e.g. extremely large area)."""
    assert preprocessor.validate_area(15000) is False

def test_hash_neighborhood_deterministic(preprocessor):
    """
    Ensure hashing logic is deterministic.
    Same input must always produce the same bucket index.
    """
    input_neighborhood = "Kadikoy"
    result1 = preprocessor.hash_neighborhood(input_neighborhood)
    result2 = preprocessor.hash_neighborhood(input_neighborhood)
    
    # 1. Consistency check
    assert result1 == result2
    # 2. Range check
    assert 0 <= result1 < 100

def test_hash_neighborhood_standardization(preprocessor):
    """Verify input standardization (case and whitespace independence)."""
    res1 = preprocessor.hash_neighborhood("kadikoy")
    res2 = preprocessor.hash_neighborhood(" KADIKOY ")
    assert res1 == res2

def test_calculate_unit_price_logic(preprocessor):
    """Verify correct calculation of unit price."""
    price = 500000
    area = 100
    expected_unit_price = 5000.0
    
    assert preprocessor.calculate_unit_price(price, area) == expected_unit_price

def test_calculate_unit_price_error(preprocessor):
    """Test zero-division protection in price calculation."""
    with pytest.raises(ValueError):
        preprocessor.calculate_unit_price(500000, 0)