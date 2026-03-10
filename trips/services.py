import requests

def validate_place_exists(external_id: str) -> bool:
    url = f"https://api.artic.edu/api/v1/artworks/{external_id}"
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False