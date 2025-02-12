# services/discount_service.py

class DiscountService:
    def calculate_discount(self, promo_code: str) -> float:
        if promo_code:
            if promo_code == "SAVE20":
                return 6  # Fixed discount amount
            else:
                raise ValueError("The provided promo code is not valid or expired.")
        return 0
