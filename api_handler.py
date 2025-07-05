import requests

# Example function to send a GET request to an external API
def fetch_external_info(endpoint):
    try:
        response = requests.get(endpoint)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Status {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}
