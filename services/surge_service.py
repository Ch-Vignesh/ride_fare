# services/surge_service.py

class SurgeService:
    def apply_surge(self, subtotal: float, surge_multiplier: float) -> (float, float):
        final_fare = subtotal * surge_multiplier
        surge_adjustment = final_fare - subtotal
        return final_fare, surge_adjustment
