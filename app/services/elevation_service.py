import requests

def get_elevation(lat, lon):
    return get_elevations([(lat, lon)])[0]

def get_elevations(coordinates):
    try:
        locations = [{"latitude": lat, "longitude": lon} for lat, lon in coordinates]
        response = requests.post(
            "https://api.open-elevation.com/api/v1/lookup",
            json={"locations": locations},
            timeout=30
        )
        return [result['elevation'] for result in response.json()['results']]
    except Exception as e:
        print(f"Elevation API Error: {str(e)}")
        return [None] * len(coordinates)