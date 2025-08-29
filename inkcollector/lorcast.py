import json
import requests

class LorcastAPI():
    """
    A class to interact with the Lorcast API for collecting data on the Lorcana Trading Card Game.
    
    This class provides methods to retrieve data from the API.
    """
    def __init__(self, api_base_url="https://api.lorcast.com", api_version="v0"):
        """
        Initialize the LorcastAPI client.
        
        Parameters:
            api_base_url (str): The base URL for the Lorcast API.
            api_version (str): The version of the API to use.
        """
        self.api_url = f"{api_base_url}/{api_version}"
        self.session = requests.Session()

        # Set default headers
        self.session.headers.update({
            'User-Agent': 'InkCollector/1.0.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })

    def get_sets(self):
        """
        Retrieves a list of all card sets available in the Lorcast API.

        Returns:
            list: A list of sets, each represented as a dictionary with set details.
        """
        url = f"{self.api_url}/sets"

        try:
            response = self.session.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes

            return response.json().get('results', [])
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            raise
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON response: {e}")
            raise ValueError(f"Invalid JSON response: {e}")
    
    def get_cards(self, set_id):
        """
        Retrieves a list of cards for a specific set in the Lorcana Trading Card Game.

        Args:
            set_id (str): The ID of the set to retrieve cards from.

        Returns:
            list: A list of cards, each represented as a dictionary with card details.
        """
        api_endpoint = f"{self.api_url}/sets/{set_id}/cards"

        try:
            self.log(f"Fetching cards from Lorcast API for set {set_id}", level=logging.INFO)
            response = requests.get(api_endpoint)
            response.raise_for_status()  # Raise an error for bad responses
            # Simulate rate limiting
            time.sleep(self.api_rate_limit)
        except requests.exceptions.RequestException as e:
            self.log(f"Error fetching data from API: {str(e)}", level=logging.ERROR)
            return None
        
        if response.status_code == 200:
            cards = response.json()
        else:
            self.log(f"Response Error: {response.status_code} - {response.text}", level=logging.ERROR)
        
        self.log(f"Found {len(cards)} cards.", level=logging.INFO)
        return cards

        
    
