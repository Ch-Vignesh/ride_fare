from models import FareRequest
from services.discount_service import DiscountService
from services.surge_service import SurgeService
from services.waiting_time_service import WaitingTimeService

class FareCalculator:
    def __init__(self):
        self.discount_service = DiscountService()
        self.surge_service = SurgeService()
        self.waiting_time_service = WaitingTimeService()

    def get_base_fare_and_distance_rate(self, ride_type: str):
        if ride_type == "Standard":
            return 5, 1.2
        elif ride_type == "Premium":
            return 8, 2.0
        else:
            raise ValueError("The specified ride type is not available.")

    def calculate_additional_passenger_fee(self, passengers: int) -> float:
        # For this example, we charge $2 for every extra passenger beyond the first.
        if passengers > 1:
            return (passengers - 1) * 2
        return 0

    def calculate_fare(self, fare_request: FareRequest) -> dict:

        # Validate ride type and obtain base fare & per-km rate.
        base_fare, distance_rate = self.get_base_fare_and_distance_rate(fare_request.ride_type)
        
        # Calculate distance-based fare.
        distance_fare = fare_request.distance_km * distance_rate
        
        # Calculate time-based fare.
        time_fare = fare_request.ride_duration_minutes * 0.5
        
        # Calculate waiting time charge via the waiting time service.
        waiting_charge = self.waiting_time_service.calculate_waiting_charge(fare_request.waiting_time_minutes)
        
        # Calculate additional passenger fee.
        additional_passenger_fee = self.calculate_additional_passenger_fee(fare_request.passengers)
        
        # Calculate discount via the discount service.
        promo_discount = self.discount_service.calculate_discount(fare_request.promo_code)
        
        # Compute subtotal (before surge pricing).
        subtotal_before_surge = (
            base_fare +
            distance_fare +
            time_fare +
            waiting_charge +
            additional_passenger_fee -
            promo_discount
        )
        
        # Apply surge pricing via the surge service.
        final_fare, surge_adjustment = self.surge_service.apply_surge(subtotal_before_surge, fare_request.surge_multiplier)
        
        # Build the fare breakdown.
        fare_breakdown = {
            "base_fare": base_fare,
            "distance_fare": distance_fare,
            "time_fare": time_fare,
            "waiting_charge": waiting_charge,
            "additional_passenger_fee": additional_passenger_fee,
            "promo_discount": -promo_discount,  # negative to indicate discount
            "surge_adjustment": surge_adjustment
        }
        
        # Prepare the final ride record (to return and store).
        ride_data = {
            "ride_id": fare_request.ride_id,
            "ride_type": fare_request.ride_type,
            "pickup_location": fare_request.pickup_location,
            "dropoff_location": fare_request.dropoff_location,
            "distance_km": fare_request.distance_km,
            "ride_duration_minutes": fare_request.ride_duration_minutes,
            "waiting_time_minutes": fare_request.waiting_time_minutes,
            "passengers": fare_request.passengers,
            "promo_code": fare_request.promo_code,
            "surge_multiplier": fare_request.surge_multiplier,
            "total_fare": round(final_fare, 2),
            "fare_breakdown": fare_breakdown
        }
        return ride_data
