# models.py

from pydantic import BaseModel
from typing import Optional

class FareBreakdown(BaseModel):
    base_fare: float
    distance_fare: float
    time_fare: float
    waiting_charge: float
    additional_passenger_fee: float
    promo_discount: float
    surge_adjustment: float

class FareRequest(BaseModel):
    ride_id: int
    ride_type: str  # Expected values: "Standard" or "Premium"
    pickup_location: str
    dropoff_location: str
    distance_km: float
    ride_duration_minutes: float
    waiting_time_minutes: float
    passengers: int
    promo_code: Optional[str] = None
    surge_multiplier: float

class FareResponse(BaseModel):
    ride_id: int
    total_fare: float
    fare_breakdown: FareBreakdown
