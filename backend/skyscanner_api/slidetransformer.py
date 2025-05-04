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
    


def edit_downvote_slide(slides: list[str], order: int) -> list[str]:
    """
    Modify a specific slide in the itinerary and return the complete list of slides.
    Args:
        slides (list[str]): List of JSON strings containing all slides
        order (int): The order of the slide to modify (1-based index)
    Returns:
        list[str]: List of JSON strings, each representing a slide
    """
    try:
        # Convert string slides to JSON objects
        slides_data = [json.loads(slide) for slide in slides]
        
        # Store original slides
        original_slides = slides_data.copy()
        
        # Find the slide to modify
        target_index = None
        for i, slide in enumerate(slides_data):
            if slide.get('order') == order:
                target_index = i
                break
                
        if target_index is None:
            raise ValueError(f"No slide found with order {order}")

        # Load Gemini API key
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)

        # Prepare prompt for Gemini
        prompt = f"""Given this slide:
        {json.dumps(slides_data[target_index], indent=2)}
        
        Generate a new alternative slide with:
        - Different activity or location
        - Same time of day
        - Similar type of activity
        - Keep the same order number ({order})
        
        Return only the JSON for the new slide with format:
        {{"order": integer, "title": "string", "image_name": "string", "content": "string"}}
        Be aware that the image_name should be precise for API image search. Don't use foreign characters or emojis.
        Don't use any other text or explanation, just the JSON."""

        # Get Gemini response
        gemini_response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )

        # Clean response text
        response_text = gemini_response.text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:-3]
        elif response_text.startswith("```"):
            response_text = response_text[3:-3]

        # Parse new slide
        new_slide = json.loads(response_text)

        # Enrich only the new slide with image
        if "image_name" in new_slide:
            image_url = get_specific_image(new_slide["image_name"])
            if image_url:
                del new_slide["image_name"]
                new_slide["image_url"] = image_url["url"]
            else:
                new_slide["image_url"] = f"No image found for: {new_slide['image_name']}"
                del new_slide["image_name"]

        # Replace old slide with new one
        slides_data[target_index] = new_slide

        # Convert back to JSON strings
        slide_strings = [json.dumps(slide, ensure_ascii=False) for slide in slides_data]

        # Save updated slides to file
        output_dir = os.path.join(os.path.dirname(__file__), "outputs")
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = os.path.join(output_dir, "slides.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(slide_strings, f, indent=2, ensure_ascii=False)

        return slide_strings

    except Exception as e:
        print(f"Error editing slide: {str(e)}")
        return slides  # Return original slides if there's an error

if __name__ == "__main__":
    # Test example - properly formatted as a list of JSON strings
    example_slides = [
        json.dumps({
            "order": 1,
            "title": "Welcome to Fernando de Noronha!",
            "content": "Get ready for an unforgettable trip to the breathtaking archipelago of Fernando de Noronha, Brazil!",
            "image_url": "https://images.pexels.com/photos/12271415/pexels-photo-12271415.jpeg"
        }),
        json.dumps({
            "order": 2,
            "title": "Day 1: Morning - Baia do Sancho Exploration",
            "content": "Start your day with a visit to Baia do Sancho, consistently ranked as one of the world's best beaches.",
            "image_url": "https://images.pexels.com/photos/4282672/pexels-photo-4282672.jpeg"
        }),
        json.dumps({
            "order": 3,
            "title": "Day 1: Afternoon - Praia do Leão Relaxation",
            "content": "In the afternoon, head to Praia do Leão, known for its dramatic landscape and nesting sea turtles.",
            "image_url": "https://images.pexels.com/photos/4282672/pexels-photo-4282672.jpeg"
        })
    ]
    
    # Test editing slide 3
    print(edit_downvote_slide(example_slides, 3))



