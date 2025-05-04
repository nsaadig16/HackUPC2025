import argparse
import json
import os
import sys
from typing import Dict, Any, Optional

import requests
from dotenv import load_dotenv


def create_search_session(api_key: str) -> Optional[Dict[str, Any]]:
    """
    Create a flight search session using Skyscanner API.

    Args:
        api_key (str): Your Skyscanner API key

    Returns:
        Optional[Dict[str, Any]]: The JSON response from the API or None if the request fails
    """
    url = "https://partners.api.skyscanner.net/apiservices/v3/flights/live/search/create"

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "query": {
            "market": "UK",
            "locale": "en-GB",
            "currency": "GBP",
            "query_legs": [
                {
                    "origin_place_id": {"iata": "BCN"},
                    "destination_place_id": {"iata": "SZX"},
                    "date": {"year": 2025, "month": 10, "day": 30}
                }
            ],
            "adults": 1,
            "cabin_class": "CABIN_CLASS_ECONOMY"
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response: {response.text if 'response' in locals() else 'No response'}")
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")

    return None


def poll_search_results(api_key: str, session_token: str) -> Optional[Dict[str, Any]]:
    """
    Poll for flight search results using the session token.

    Args:
        api_key (str): Your Skyscanner API key
        session_token (str): Session token from create search response

    Returns:
        Optional[Dict[str, Any]]: The JSON response from the API or None if the request fails
    """
    url = f"https://partners.api.skyscanner.net/apiservices/v3/flights/live/search/poll/{session_token}"

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response: {response.text if 'response' in locals() else 'No response'}")
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")

    return None


def main() -> None:
    # Load environment variables from .env file
    load_dotenv()

    parser = argparse.ArgumentParser(description="Search for flights using Skyscanner Live Search API")
    parser.add_argument("--api-key",
                        default=os.environ.get("SKYSCANNER_API_KEY", "your-api-key"),
                        help="Your Skyscanner API key (defaults to SKYSCANNER_API_KEY from .env)")
    args = parser.parse_args()

    # Step 1: Create search session
    print("Creating search session...")
    create_response = create_search_session(args.api_key)

    if not create_response:
        print("Failed to create search session")
        sys.exit(1)

    # Extract session token
    session_token = create_response.get("sessionToken")
    if not session_token:
        print("Session token not found in response")
        print(json.dumps(create_response, indent=4))
        sys.exit(1)

    print(f"Session created. Token: {session_token}")

    # Step 2: Poll for results
    print("Polling for search results...")
    poll_response = poll_search_results(args.api_key, session_token)

    if poll_response:
        print(json.dumps(poll_response, indent=4))
    else:
        print("Failed to retrieve search results")
        sys.exit(1)


if __name__ == "__main__":
    main()