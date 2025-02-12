
from fastapi import FastAPI, HTTPException, status
from models import FareRequest, FareResponse
from services.fare_calculator import FareCalculator
from database import MongoDBClient

app = FastAPI(title="Ride Fare Estimation API")

# Initialize the MongoDB client (singleton)
db_client = MongoDBClient()

# Instantiate the fare calculator service
fare_calculator = FareCalculator()

# CREATE (POST)
@app.post("/estimate_fare", response_model=FareResponse, status_code=status.HTTP_201_CREATED)
def create_ride(fare_request: FareRequest):
    try:
        # Calculate the fare and prepare ride data
        ride_data = fare_calculator.calculate_fare(fare_request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Insert the ride record into MongoDB
    db_client.insert_ride(ride_data)
    return ride_data

# READ (GET) - Single Record
@app.get("/ride/{ride_id}", response_model=FareResponse)
def get_ride(ride_id: int):
    ride = db_client.find_ride_by_id(ride_id)
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")
    # Remove MongoDB internal _id field if present
    ride.pop("_id", None)
    return ride

# READ (GET) - All Records
@app.get("/rides", response_model=list[FareResponse])
def get_all_rides():
    rides = db_client.find_all_rides()
    for ride in rides:
        ride.pop("_id", None)
    return rides

# UPDATE (PUT)
@app.put("/ride/{ride_id}", response_model=FareResponse)
def update_ride(ride_id: int, fare_request: FareRequest):
    # Ensure the ride exists
    existing_ride = db_client.find_ride_by_id(ride_id)
    if not existing_ride:
        raise HTTPException(status_code=404, detail="Ride not found")
    
    # Ensure the ride_id in the payload matches the URL
    if fare_request.ride_id != ride_id:
        raise HTTPException(status_code=400, detail="Ride ID in URL and body do not match")
    
    # Recalculate fare with the updated data
    try:
        updated_ride_data = fare_calculator.calculate_fare(fare_request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Update record in MongoDB
    db_client.update_ride(ride_id, updated_ride_data)
    return updated_ride_data

# DELETE (DELETE)
@app.delete("/ride/{ride_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ride(ride_id: int):
    result = db_client.delete_ride(ride_id)
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Ride not found")
    return {"detail": "Ride deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
