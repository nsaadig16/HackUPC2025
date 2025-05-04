import os
import json
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from google import genai
from routers.pexels import get_specific_image

def generate_slides_with_images(itinerary: str) -> list[str]:
    """
    Generate slides with images from an itinerary and return as list of JSON strings.
    
    Args:
        itinerary (str): JSON string containing the travel itinerary
        
    Returns:
        list[str]: List of JSON strings, each representing a slide
    """
    try:
        # Load Gemini API key
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)

        # Send to Gemini
        prompt = """You will be given an itinerary with the following format: {
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
        
        Create 7 slides: First slide about destination, then 6 slides for 3 days (morning/afternoon each).
        Return only JSON array with format:
        [{"order": integer, "title": "string", "image_name": "string", "content": "string"}]
        image_name should be precise for API image search."""

        # Get Gemini response
        gemini_response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt + f"\nActual input: {itinerary}",
        )

        # Clean response text
        response_text = gemini_response.text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:-3]
        elif response_text.startswith("```"):
            response_text = response_text[3:-3]

        # Parse slides
        slides = json.loads(response_text)

        # Enrich with images
        for slide in slides:
            if "image_name" in slide:
                image_url = get_specific_image(slide["image_name"])
                if image_url:
                    del slide["image_name"]
                    slide["image_url"] = image_url["url"]
                else:
                    slide["image_url"] = f"No image found for: {slide['image_name']}"
                    del slide["image_name"]

        # Convert each slide to JSON string
        slide_strings = [json.dumps(slide, ensure_ascii=False) for slide in slides]

        # Save to file (optional)
        output_dir = os.path.join(os.path.dirname(__file__), "outputs")
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = os.path.join(output_dir, "slides.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(slide_strings, f, indent=2, ensure_ascii=False)

        return slide_strings

    except Exception as e:
        print(f"Error generating slides: {str(e)}")
        return [json.dumps({"error": str(e)})]