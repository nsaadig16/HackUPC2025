import os
from typing import Optional
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

# Load environment variables
load_dotenv()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def get_specific_image(subject: str = "Paris") -> Optional[dict]:
    """
    Fetch a specific image from Pexels API
    """
    headers = {
        "Authorization": PEXELS_API_KEY
    }
    
    url = f"https://api.pexels.com/v1/search?query={subject}&orientation=landscape&per_page=1"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        if data["photos"]:
            return {
                "url": data["photos"][0]["src"]["original"],
            }
        return None
    
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/specific-image")
async def get_specific_image_endpoint():
    """
    Endpoint to get a specific image (default: zebra)
    """
    image_data = get_specific_image()
    if not image_data:
        raise HTTPException(status_code=404, detail="No image found")
    
    return JSONResponse(content=image_data)