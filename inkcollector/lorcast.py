import requests

class Lorcast:
    def __init__(self):
        self.name = "lorcast"
        self.description = "Collects data from the Lorecast API."
        self.api_base_url = "https://api.lorcast.com"
        self.api_base_url = "https://api.lorcast.com"
        self.api_current_version = "v0"
        self.api_rate_limit = 5 # delay per request in seconds
        self.api_url = f"{self.api_base_url}/{self.api_current_version}"

    def get_sets(self):
        """
        Retrieves a list of all card sets available in the Lorcana Trading Card Game, including both standard and promotional sets.

        Returns:
            list: A list of sets, each represented as a dictionary with set details.
        """
        api_endpoint = f"{self.api_url}/sets"

        try:
            print(f"Fetching sets form Lorcast API")
            response = requests.get(api_endpoint)
            response.raise_for_status()  # Raise an error for bad responses
        except requests.exceptions.RequestException as e:
            # Print the error message
            print(f"Error fetching data from API: {str(e)}")
            return None
        
        if response.status_code == 200:
            data = response.json()
        else:
            print(f"Response Error: {response.status_code} - {response.text}")

        sets = data.get("results", None)

        if not sets:
            print("No sets found.")
        
        print(f"Found {len(sets)} sets.")
        return sets

        
    
