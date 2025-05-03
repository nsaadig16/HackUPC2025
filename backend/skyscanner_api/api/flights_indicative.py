import requests
import json
import argparse
import sys
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv


def search_flights(
    api_key: str,
    origin: str,
    destination: str,
    market: str = "ES",
    locale: str = "en-GB",
    currency: str = "EUR",
    anytime: bool = True
) -> Optional[Dict[str, Any]]:
    """
    Search for indicative flight prices using Skyscanner API.

    Args:
        api_key (str): Your Skyscanner API key
        origin (str): IATA code for the origin airport (e.g., "BCN" for Barcelona)
        destination (str): IATA code for the destination airport (e.g., "JFK" for New York JFK)
        market (str): Market country code (e.g., "ES" for Spain)
        locale (str): Locale for results (e.g., "en-GB" for British English)
        currency (str): Currency for prices (e.g., "EUR" for Euros)
        anytime (bool): Whether to search for flights at any time

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
            "market": market,
            "locale": locale,
            "currency": currency,
            "queryLegs": [
                {
                    "originPlace": {
                        "queryPlace": {
                            "iata": origin
                        }
                    },
                    "destinationPlace": {
                        "queryPlace": {
                            "iata": destination
                        }
                    },
                    "anytime": anytime
                }
            ]
        }
    }

    try:
        # Make the POST request
        response: requests.Response = requests.post(url, headers=headers, json=payload)

        # Check if the request was successful
        response.raise_for_status()
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


def main() -> None:
    # Load environment variables from .env file
    load_dotenv()

    parser = argparse.ArgumentParser(description="Search for flights using Skyscanner API")
    parser.add_argument("--api-key",
                        default=os.environ.get("SKYSCANNER_API_KEY", "your-api-key"),
                        help="Your Skyscanner API key (defaults to SKYSCANNER_API_KEY from .env)")
    parser.add_argument("--origin", default="BCN", help="IATA code for origin airport (default: BCN)")
    parser.add_argument("--destination", default="JFK", help="IATA code for destination airport (default: JFK)")
    parser.add_argument("--market", default="ES", help="Market country code (default: ES)")
    parser.add_argument("--locale", default="en-GB", help="Locale for results (default: en-GB)")
    parser.add_argument("--currency", default="EUR", help="Currency for prices (default: EUR)")
    parser.add_argument("--fixed-dates", action="store_false", dest="anytime", 
                      help="Search for specific dates instead of anytime")
    args = parser.parse_args()

    # Search for flights
    results: Optional[Dict[str, Any]] = search_flights(
        args.api_key,
        args.origin,
        args.destination,
        args.market,
        args.locale,
        args.currency,
        args.anytime
    )

    # Print results (if successful)
    if results:
        print(json.dumps(results, indent=4))
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()