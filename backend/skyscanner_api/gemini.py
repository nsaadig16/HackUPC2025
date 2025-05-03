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
    prompt = """
    I want you to **only** give me the output with the structure below, no explanations, no extra comments.

    Input: One or more JSON objects with the following fields:
    - username (string)
    - destination (string or null)
    - origin (string)
    - language (string)
    - cabin_class (string)
    - disponibility (tuple of two dates: start_date, end_date)
    - max_price (integer)
    - hire_car (boolean)
    - hotel (boolean)
    - preferences (list of strings)

    If the destination is null, choose the best destination according to the traveler's preferences.

    Give me a list of 5 destinations with the best price, that:
    - Takes into account all preferences from all travelers in the group.
    - Selects the best available options (flights, hotels, hire cars) for each traveler.
    - Makes sure the arrival date and departure date are the same for everyone, since they travel together at the destination. Also add the IATA code of the origin and destination.

    Output format (strictly this JSON structure):
    {
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
            "price": integer,
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

    Example Input:
    {
    "inputs": [
        {
        "username": "Julliz",
        "destination": null,
        "origin": "spain",
        "language": "catalan",
        "cabin_class": "business",
        "disponibility": ["2025-06-10", "2025-06-17"],
        "max_price": 1000,
        "hire_car": true,
        "hotel": true,
        "preferences": ["mountain", "nightlife", "culture and art"]
        }
    ]
    }

    Example Output:
    {
    "itineraries": [
        {
        "destination": "Barcelona, Spain",
        "flights": [
            {
            "origin": "Moscow, Russia",
            "destination": "Barcelona, Spain",
            "IATA_origin": "DME",
            "IATA_destination": "BCN",
            "departure_date": "2025-06-12",
            "arrival_date": "2025-06-12",
            "price": 150,
            "cabin_class": "business",
            "airline": "Air France"
            },
            {
            "origin": "Naples, Italy",
            "destination": "Barcelona, Spain",
            "IATA_origin": "NAP",
            "IATA_destination": "BCN",
            "departure_date": "2025-06-12",
            "arrival_date": "2025-06-12",
            "price": 80,
            "cabin_class": "economy",
            "airline": "Vueling"
            }
        ],
        "hotel": {
            "name": "Hotel Arts Barcelona",
            "price": 560
        },
        "hire_car": {
            "company": "Sixt",
            "price": 150
        }
        },
        {
        "destination": "Ljubljana, Slovenia",
        "flights": [
            {
            "origin": "Barcelona, Spain",
            "destination": "Ljubljana, Slovenia",
            "IATA_origin": "BCN",
            "IATA_destination": "LJU",
            "departure_date": "2025-06-12",
            "arrival_date": "2025-06-12",
            "price": 180,
            "cabin_class": "business",
            "airline": "Lufthansa"
            },
            {
            "origin": "Italy, Naples",
            "destination": "Ljubljana, Slovenia",
            "IATA_origin": "NAP",
            "IATA_destination": "LJU",
            "departure_date": "2025-06-12",
            "arrival_date": "2025-06-12",
            "price": 90,
            "cabin_class": "economy",
            "airline": "ITA Airways"
            }
        ]
    ]
    }
    """
    
    # Step 4: Send to Gemini
    gemini_response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt,
    )

    # Step 5: Print the result
    print(gemini_response.text)
    return gemini_response.text

def search_flights(api_key: str, origin : str, destination : str) -> Optional[Dict[str, Any]]:

    """
    Search for indicative flight prices using Skyscanner API.

    Args:
        api_key (str): Your Skyscanner API key

    Returns:
        Optional[Dict[str, Any]]: The JSON response from the API or None if the request fails
    """
    # API endpoint
    url: str = "https://partners.api.skyscanner.net/apiservices/v3/flights/indicative/search"

    # Headers
    headers: Dict[str, str] = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }

    # Request payload
    payload: Dict[str, Any] = {
        "query": {
            "market": "ES",
            "locale": "en-GB",
            "currency": "EUR",
            "queryLegs": [
                {
                    "originPlace": {
                        "queryPlace": {
                            "iata": f"{origin}"
                        }
                    },
                    "destinationPlace": {
                        "queryPlace": {
                            "iata": f"{destination}"
                        }
                    },
                    "anytime": True
                }
            ]
        }
    }

    try:
        # Make the POST request
        response: requests.Response = requests.post(url, headers=headers, json=payload)

        # Check if the request was successful
        response.raise_for_status()
        print(f"Successfully retrieved flight data from {origin} to {destination}")
        return response.json()
        
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response: {response.text if 'response' in locals() else 'No response'}")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: {e}")
    except requests.exceptions.Timeout as e:
        print(f"Timeout Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")

    return None

def process_gemini_and_search_flights(gemini_response_text: str, api_key: str) -> List[Dict[str, Any]]:
    """
    Process the Gemini API response and search for flights using the Skyscanner API.
    
    Args:
        gemini_response_text (str): The response from the Gemini API
        api_key (str): Your Skyscanner API key
        
    Returns:
        List[Dict[str, Any]]: List of flight search results
    """
    # Clean the Gemini response text by removing Markdown code block markers
    cleaned_response = gemini_response_text.strip()
    if cleaned_response.startswith("```json"):
        cleaned_response = cleaned_response[7:]
    elif cleaned_response.startswith("```"):
        cleaned_response = cleaned_response[3:]
    
    if cleaned_response.endswith("```"):
        cleaned_response = cleaned_response[:-3]
    
    cleaned_response = cleaned_response.strip()
    
    # Parse the cleaned Gemini response
    try:
        gemini_data = json.loads(cleaned_response)
        flight_results = []
        
        # Process each itinerary
        for itinerary in gemini_data.get("itineraries", []):
            destination_iata = None
            
            # Process each flight in the itinerary
            for flight in itinerary.get("flights", []):
                origin_iata = flight.get("IATA_origin")
                destination_iata = flight.get("IATA_destination")
                
                # Skip if IATA codes are missing
                if not origin_iata or not destination_iata:
                    print(f"Missing IATA codes for flight from {flight.get('origin')} to {flight.get('destination')}")
                    continue
                
                # Call the search_flights function using IATA codes
                search_result = search_flights(api_key, origin_iata, destination_iata)
                if search_result:
                    # Extract data from API response
                    content = search_result.get('content', {})
                    results = content.get('results', {})
                    quotes = results.get('quotes', {})
                    
                    # Get pricing info from the API if available
                    api_price = None
                    cheapest_quote_id = None
                    if quotes:
                        # Find the cheapest quote
                        for quote_id, quote in quotes.items():
                            price = quote.get('price', {}).get('amount')
                            if price and (api_price is None or price < api_price):
                                api_price = price
                                cheapest_quote_id = quote_id
                    
                    # Extract carrier info if available
                    api_airline = None
                    if cheapest_quote_id and 'carriers' in results:
                        quote = quotes.get(cheapest_quote_id, {})
                        carrier_ids = []
                        
                        # Get carrier IDs from the cheapest quote
                        for leg in quote.get('legs', []):
                            for segment in leg.get('segments', []):
                                carrier_id = segment.get('marketingCarrierId')
                                if carrier_id:
                                    carrier_ids.append(carrier_id)
                        
                        # Get carrier name from the first ID
                        if carrier_ids and results.get('carriers'):
                            carrier = results.get('carriers', {}).get(str(carrier_ids[0]), {})
                            api_airline = carrier.get('name')
                    
                    # Extract useful flight information, using API data where available
                    flight_info = {
                        "origin": flight.get("origin"),
                        "destination": flight.get("destination"),
                        "origin_iata": origin_iata,
                        "destination_iata": destination_iata,
                        "departure_date": flight.get("departure_date"),
                        "arrival_date": flight.get("arrival_date"),
                        "price": api_price if api_price else flight.get("price"),
                        "airline": api_airline if api_airline else flight.get("airline"),
                        "cabin_class": flight.get("cabin_class"),
                        "search_result": search_result
                    }
                    flight_results.append(flight_info)
        
        return flight_results
    
    except json.JSONDecodeError as e:
        print(f"Error parsing Gemini response: {e}")
        print(f"Response text: {gemini_response_text}")
        return []
    except Exception as e:
        print(f"Error processing Gemini response: {e}")
        return []

if __name__ == "__main__":
    # Example of how to use the function
    load_dotenv()
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    skyscanner_api_key = os.getenv("SKYSCANNER_API_KEY")
    
    # Example: Call Gemini and then search flights
    gemini_result = call_gemini_api(gemini_api_key)
    flight_results = process_gemini_and_search_flights(gemini_result, skyscanner_api_key)
    
    print(f"Found {len(flight_results)} flight results")
    # Print results with more detailed information
    for result in flight_results:
        print("\n" + "=" * 50)
        print(f"Flight from {result['origin']} ({result['origin_iata']}) to {result['destination']} ({result['destination_iata']})")
        print(f"Departure: {result['departure_date']}, Arrival: {result['arrival_date']}")
        print(f"Price: €{result['price']}")
        print(f"Airline: {result['airline']}, Class: {result['cabin_class']}")
        
        # Display some API search result data if available
        if result['search_result']:
            content = result['search_result'].get('content', {})
            results = content.get('results', {})
            quotes = results.get('quotes', {})
            
            print("\nAvailable quotes from Skyscanner API:")
            count = 0
            if quotes:
                # Handle quotes as a dictionary instead of a list
                for quote_id, quote in quotes.items():
                    price = quote.get('price', {}).get('amount')
                    if price:
                        count += 1
                        print(f"  Quote {count}: €{price}")
                        if count >= 3:  # Show up to 3 quotes
                            break