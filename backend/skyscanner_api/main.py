from fastapi import FastAPI, HTTPException
from api.flights_indicative import search_flights
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional
from fastapi import status
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from routers import pexels


app = FastAPI()

# Load routers
app.include_router(pexels.router, prefix="/pexels", tags=["Pexels"])
class Travel(BaseModel):
      username: str
      destination: Optional[list[str]] = []
      origin: str
      language: list[str]
      disponibility: list[str]
      max_price: int
      hire_car: bool
      hotel: bool
      preferences: Optional[list[str]] = []

class Slide(BaseModel):
      order: int
      title: str
      image_url: str
      content: str

travel_list = [Travel(username="Julliz",destination=[],origin="Perú",language=["spanish"],disponibility=["2025-06-10", "2025-06-17"], max_price=2500, hire_car=True, hotel=True, preferences=["beach", "underrated locations"]),
              Travel(username="Oggy",destination=[],origin="Nigeria",language=["Arabe"],disponibility=["2025-06-10", "2025-07-1"], max_price=10000, hire_car=False, hotel=True, preferences=["mountain", "nightlife", "culture and art"]),
              Travel(username="Lolo",destination=[],origin="Londres",language=["english"],disponibility=["2025-04-10", "2025-07-20"], max_price=1500, hire_car=False, hotel=False, preferences=["old cities", "culture and art"]),]


@app.get("/")
def read_root():
    return {"message": "Welcome to HackUPC2025!"}

@app.get("/travel/")
async def users():
    return travel_list

@app.post("/travel/", response_model=Travel, status_code=201)
async def travel(travel: Travel):
    if type(search_username(travel.username)) == Travel:
        raise HTTPException(status_code=404, detail="El usuario ya existe")
 
    if travel.destination is None:
        travel.destination = []
    if travel.preferences is None:
        travel.preferences = []
        
    travel_list.append(travel)
    return travel

@app.put("/travel/{username}", status_code=202)
async def travel(travel: Travel):

    found = False

    for index,saved_travel in enumerate(travel_list):
        if saved_travel.username == travel.username:
            travel_list[index] = travel
            found = True

    if not found:
        raise HTTPException(status_code=404, detail="El usuario no existe")

    return travel

@app.delete("/travel/{username}", status_code=204)
async def travel(username: str):

    found = False


    for index,saved_travel in enumerate(travel_list):
        if saved_travel.username == username:
            del travel_list[index]
            found = True
    if not found:
        raise HTTPException(status_code=404, detail="El usuario no existe")

travels=[]

@app.post("/travel/{travel}")
async def save_travel(travel: str): #! IMPORTANT: 
        
    travel_list.append(travel)
    return travel
    
def search_username(username: str):
    travelers = filter(lambda travel: travel.username == username, travel_list)
    try:
        return list(travelers)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}

slides = [
    Slide(order=1, title="Bienvenida", image_url='https://example.com', content="Bienvenido a la API de viajes."),
    Slide(order=2, title="Destinos", image_url='https://example.com',content="Explora nuestros destinos recomendados."),
    Slide(order=3, title="Reservas", image_url='https://example.com',content="Realiza tu reserva en línea."),
]


@app.get("/slide/{order}", status_code=200)
async def get_slide(order: int):
    for slide in slides:
        if slide.order == order:
            return slide
    raise HTTPException(status_code=404, detail="Slide not found")

