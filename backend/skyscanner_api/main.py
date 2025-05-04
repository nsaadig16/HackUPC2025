import json
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
from slidetransformer import edit_downvote_slide, generate_slides_with_images
from gemini import get_itinerary
#from slidetransformer import make_slides
from routers import pexels
from sqliteconnect import SQLiteConnector as SQLiteConnect
from Travel import Travel
app = FastAPI()

# Load routers
app.include_router(pexels.router, prefix="/pexels", tags=["Pexels"])


class Slide(BaseModel):
      order: int
      title: str
      image_url: str
      content: str

@app.get("/")
def read_root():
    return {"message": "Welcome to HackUPC2025!"}

@app.get("/travel")
async def travel():
    return SQLiteConnect.get_all("travel")


@app.get("/numtravels", status_code=200)
async def get_num_travels():
    travels = SQLiteConnect.get_all("travel")
    return {"num_travels": len(travels)}

@app.post("/travel", response_model=Travel, status_code=201)
async def travel(travel: Travel):
    travel.id = SQLiteConnect.insert("travel", travel.dict())
    return travel

# @app.put("/travel/{username}", status_code=202)
# async def travel(travel: Travel):

#     found = False

#     for index,saved_travel in enumerate(travel_list):
#         if saved_travel.username == travel.username:
#             travel_list[index] = travel
#             found = True

#     if not found:
#         raise HTTPException(status_code=404, detail="El usuario no existe")

#     return travel

@app.delete("/travel/{id}", status_code=204)
async def travel(id: int):
    SQLiteConnect.delete("travel", id)
    return True

@app.post("/finish", status_code=200)
async def finish():
    travels = SQLiteConnect.get_all("travel")
    itin = get_itinerary('',travels)
    SQLiteConnect.insert("itinerary", itin)
    slides = generate_slides_with_images(itin)
    SQLiteConnect.insert("slides", slides)
    flights = search_flights(itin)
    SQLiteConnect.insert("flight", flights)

@app.get("/flights", status_code=200)
async def get_flights():
    return SQLiteConnect.get_all("flight")
    

@app.get("/slide/{order}", status_code=200)
async def get_slide(order: int):
    return SQLiteConnect.get_by_order("slides", order)

@app.get("/slides", status_code=200)
async def get_slides():
    return SQLiteConnect.get_all("slides")


order = 1
@app.get("/next_slide", status_code=200)
async def get_next_slide():
    if order == 1:
        slides = SQLiteConnect.get_by_order("slides", order)
        return json.loads(slides.content)
    else:
        slides = SQLiteConnect.get_by_order("slides", order)
        voutes = slides.votes_up + slides.votes_down
        if voutes == len(SQLiteConnect.get_all("travel")):
            if slides.votes_up > slides.votes_down:
                slides = edit_downvote_slide(slides.content, order)
                slides=SQLiteConnect.replace("slides", order, slides)
            else:
                order += 1
                slides = SQLiteConnect.get_by_order("slides", order)
            return json.loads(slides.content)
        return json.loads(slides.content)
