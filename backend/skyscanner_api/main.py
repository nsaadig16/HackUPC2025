from fastapi import FastAPI, HTTPException
from api.flights_indicative import search_flights
import os
from dotenv import load_dotenv
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to HackUPC2025!"}

@app.get("/flights/origin/{origin}/destination/{destination}")
def get_flights(origin: str, destination: str):
    """
    Endpoint to get indicative flight prices.
    """
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("SKYSCANNER_API_KEY")
    
    if not api_key:
        raise HTTPException(status_code=400, detail="API key not found in environment variables.")
    
    # Call the search_flights function
    result = search_flights(api_key, origin, destination)
    
    if result is None:
        raise HTTPException(status_code=400, detail="Failed to fetch flight data.")
    
    return result