import requests, dotenv, os, sys

def call_api(endpoint : str):
    url = 'https://partners.api.skyscanner.net/apiservices/v3/' + endpoint

    dotenv.load_dotenv()
    # Cargar la API key desde el archivo .env
    api_key = os.getenv("SKYSCANNER_API_KEY")
    if not api_key:
        print("ERROR: No se encontró la API key. Asegúrate de tener un archivo .env con SKYSCANNER_API_KEY")
        return None
    headers = {
        'x-api-key': api_key  # replace with your actual API key
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print (response.json())  # or response.text if you prefer raw output
    else:
        print(f'Failed with status code: {response.status_code}')

if __name__ == "__main__":
    endpoint = sys.argv[1]
    call_api(endpoint)