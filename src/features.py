import hashlib

class HousePricePreprocessor:
    """Feature engineering and validation logic for house price prediction."""

    def __init__(self, num_buckets=100):
        self.num_buckets = num_buckets

    def validate_area(self, area_m2: float) -> bool:
        """
        Validates property area limits.
        Returns False for outliers (>10,000 m2).
        """
        if area_m2 <= 0:
            raise ValueError("Area must be greater than 0.")
        
        if area_m2 > 10000:
            return False 
            
        return True

    def hash_neighborhood(self, neighborhood: str) -> int:
        """
        Transforms neighborhood name into a bucket index (Hashing Trick).
        Useful for handling high-cardinality categorical features.
        """
        if not isinstance(neighborhood, str):
            raise TypeError("Neighborhood name must be a string.")
        
        # Standardize string (lower case + trim)
        clean_name = neighborhood.lower().strip()
        
        # Deterministic SHA256 hashing
        hash_object = hashlib.sha256(clean_name.encode('utf-8'))
        hex_dig = hash_object.hexdigest()
        
        return int(hex_dig, 16) % self.num_buckets

    def calculate_unit_price(self, total_price: float, area_m2: float) -> float:
        """Calculates price per square meter (Feature Engineering)."""
        if area_m2 <= 0:
            raise ValueError("Area must be positive to calculate unit price.")
            
        return total_price / area_m2