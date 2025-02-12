# services/waiting_time_service.py

class WaitingTimeService:
    def calculate_waiting_charge(self, waiting_minutes: float) -> float:
        return waiting_minutes * 0.3
