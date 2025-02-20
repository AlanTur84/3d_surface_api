import requests

def get_elevation(lat, lon):
    try:
        response = requests.post(
            "https://api.open-elevation.com/api/v1/lookup",
            json={"locations": [{"latitude": lat, "longitude": lon}]},
            timeout=10
        )
        response.raise_for_status()
        return response.json()['results'][0]['elevation']
    except requests.exceptions.RequestException as e:
        print(f"Elevation API Error: {str(e)}")
        return None