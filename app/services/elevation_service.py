import requests
from tenacity import retry, stop_after_attempt, wait_fixed

@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def get_elevations(coordinates):
    try:
        locations = [{"latitude": lat, "longitude": lon} for lat, lon in coordinates]
        response = requests.post(
            "https://api.open-elevation.com/api/v1/lookup",
            json={"locations": locations},
            timeout=10
        )
        response.raise_for_status()
        return [result['elevation'] for result in response.json()['results']]
    except requests.exceptions.RequestException as e:
        print(f"Elevation API Error: {str(e)}")
        return [None] * len(coordinates)