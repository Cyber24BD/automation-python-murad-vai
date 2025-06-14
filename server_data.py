import requests

def fetch_data_from_server():
    # Replace this URL with your actual localhost server URL and port
    url = "http://localhost:8510/json"  # Update the port and endpoint as needed
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()  # Parse JSON response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from server: {e}")
        return []

# Fetch data from the server
multi_config = fetch_data_from_server()

# If you want to see the data (for testing)
print("Fetched data:", multi_config)