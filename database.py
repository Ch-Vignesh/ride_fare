# database.py

from pymongo import MongoClient

class MongoDBClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBClient, cls).__new__(cls)
            cls._instance.client = MongoClient("mongodb://localhost:27017")
            cls._instance.db = cls._instance.client["ride_fare_db"]
            cls._instance.collection = cls._instance.db["rides"]
        return cls._instance

    def insert_ride(self, ride_data: dict):
        self.collection.insert_one(ride_data)
        
    def find_ride_by_id(self, ride_id: int) -> dict:
        return self.collection.find_one({"ride_id": ride_id})
    
    def find_all_rides(self) -> list:
        return list(self.collection.find())
    
    def update_ride(self, ride_id: int, update_data: dict):
        self.collection.update_one({"ride_id": ride_id}, {"$set": update_data})
    
    def delete_ride(self, ride_id: int):
        return self.collection.delete_one({"ride_id": ride_id})
