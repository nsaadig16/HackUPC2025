import os
import requests
import json
from dotenv import load_dotenv
from google import genai
from api.flights_indicative import search_flights
from typing import Dict, Any, Optional, List


def call_gemini_api(api_key : str):

    """
    Call the Gemini API with the provided prompt.
    """
    # Load Gemini API key
    load_dotenv()
    client = genai.Client(api_key=api_key)

    # Step 3: Build the prompt - using regular string instead of f-string to avoid format issues
    prompt = "Generate a presentation in pdf about a trip to Paris. Generate a slide for each of the days"       
    # Step 4: Send to Gemini
    gemini_response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt,
    )

    # Step 5: Print the result
    print(gemini_response.text)
    return gemini_response.text
