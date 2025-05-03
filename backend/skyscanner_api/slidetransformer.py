import os
import requests
import json
from dotenv import load_dotenv
from google import genai
from api.flights_indicative import search_flights
from typing import Dict, Any, Optional, List
from routers.pexels import get_specific_image

def make_slides( input : str) -> str:

    """
    Call the Gemini API with the provided prompt.
    """
    # Load Gemini API key
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
 
    
    # Step 4: Send to Gemini
    gemini_response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents="""You will be given an itinerary with the following format: {
        "itineraries": [
            {
            "destination": "string",
            "flights": [
                {
                "origin": "string",
                "destination": "string",
                "IATA_origin": "string",
                "IATA_destination": "string",
                "departure_date": "YYYY-MM-DD",
                "arrival_date": "YYYY-MM-DD",
                "cabin_class": "string",
                "airline": "string"
                }
            ],
            "hotel": {
                "name": "string",
                "price": integer
            },
            "hire_car": {
                "company": "string",
                "price": integer
            }
            }
        ]
        }
        
        You will be asked to create a slide for the itinerary. The slides should contain this: The first slide will be the destination location. The next 6 slides will be a plan for the three days (1st day morning, 1st day afternoon, 2nd day morning, 2nd day afternoon, 3rd day morning, 3rd day afternoon). The slides should be in the following format:
        {"order": integer, "title": "string", "image_name": "string", "content": "string"} The image name should be precise and related to the content, since it will be sent to an API image. The title should be a short description of the content. The content should explain an activity or a place to visit, with prices. The order should be the number of the slide. The first slide should be 1, the second slide should be 2, and so on. The last slide should be 7. The slides should be in English. The slides should be in JSON format. Do not add any other text or explanation. Just return the slides in JSON format. Be aware that it can't have any special characters.

        Example output:
        [
            {
                "order": 1,
                "title": "Visit the Eiffel Tower",
                "image_name": "Eiffeil Tower",
                "content": "The Eiffel Tower is one of the most iconic landmarks in Paris. You can take an elevator to the top for a stunning view of the city. The ticket price is 25 euros."
            },
            {
                "order": 2,
                "title": "Explore the Louvre Museum",
                "image_name": "Louvre Museum",
                "content": "The Louvre Museum is the world's largest art museum and a historic monument in Paris. You can see the Mona Lisa and other famous artworks. The ticket price is 17 euros."
            }
        ]
        """ + f"Actual input: {input}",
    )

    # Step 5: Print the result
    
    response_text = gemini_response.text
    if response_text.startswith("```json") and response_text.endswith("```"):
        response_text = response_text[7:-3]  # Remove ```json from start and ``` from end
    elif response_text.startswith("```") and response_text.endswith("```"):
        response_text = response_text[3:-3] 
    return response_text.strip()

def enrich_slides_with_images(slides_json: str) -> str:
    """
    Replace image_name with image_url in the slides JSON by fetching images from Pexels API
    """
    try:
        # Parse the JSON string into a Python object
        slides = json.loads(slides_json)
        
        # Process each slide to replace image_name with image_url
        for slide in slides:
            if "image_name" in slide:
                # Get the image name
                image_name = slide["image_name"]
                
                # Fetch the image URL using the Pexels API
                image_url = get_specific_image(image_name)
                
                # Replace image_name with image_url
                if image_url:
                    del slide["image_name"]
                    slide["image_url"] = image_url
                else:
                    # If no image found, keep the original name but indicate it's a fallback
                    slide["image_url"] = f"No image found for: {image_name}"
        
        # Convert back to JSON string
        return json.dumps(slides, indent=2)
    
    except json.JSONDecodeError as e:
        print(f"Error parsing slides JSON: {str(e)}")
        return slides_json  # Return original if there's an error
    except Exception as e:
        print(f"Error enriching slides with images: {str(e)}")
        return slides_json  # Return original if there's an error


if __name__ == "__main__":
    input = """{
      "destination": "Fernando de Noronha, Brazil",
      "flights": [
        {
          "origin": "Lima, Peru",
          "destination": "Fernando de Noronha, Brazil",
          "IATA_origin": "LIM",
          "IATA_destination": "FEN",
          "departure_date": "2025-06-12",
          "arrival_date": "2025-06-12",
          "price": 800,
          "cabin_class": "business",
          "airline": "LATAM"
        }
      ],
      "hotel": {
        "name": "Pousada Maravilha",
        "price": 700
      },
      "hire_car": {
        "company": "Localiza",
        "price": 200
      }
    }"""
    # Call the function with the input
    result_no_image = make_slides(input)
    result_image = enrich_slides_with_images(result_no_image)
    # Print the result
    print(result_image)