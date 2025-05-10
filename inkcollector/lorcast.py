import logging
import requests
import time

from inkcollector import InkCollector

class Lorcast(InkCollector):
    """
    A class to interact with the Lorcast API for collecting data on the Lorcana Trading Card Game.
    
    This class provides methods to retrieve card sets and cards from the API.
    """
    def __init__(self):
        self.name = "lorcast"
        self.description = "Collects data from the Lorecast API."
        self.api_base_url = "https://api.lorcast.com"
        self.api_base_url = "https://api.lorcast.com"
        self.api_current_version = "v0"
        self.api_rate_limit = 5 # delay per request in seconds
        self.api_url = f"{self.api_base_url}/{self.api_current_version}"
        super().__init__(name=self.name)

    def get_sets(self):
        """
        Retrieves a list of all card sets available in the Lorcana Trading Card Game, including both standard and promotional sets.

        Returns:
            list: A list of sets, each represented as a dictionary with set details.
        """
        api_endpoint = f"{self.api_url}/sets"

        try:
            self.log("Fetching sets from Lorcast API", level=logging.INFO)
            response = requests.get(api_endpoint)
            # Simulate rate limiting
            time.sleep(self.api_rate_limit)
            response.raise_for_status()  # Raise an error for bad responses
        except requests.exceptions.RequestException as e:
            self.log(f"Error fetching data from API: {str(e)}", level=logging.ERROR)
            return None
        
        if response.status_code == 200:
            data = response.json()
            sets = data.get("results", None)
        else:
            self.log(f"Response Error: {response.status_code} - {response.text}", level=logging.ERROR)

        if not sets:
            self.log("No sets found.", level=logging.WARNING)
            return None
        
        self.log(f"Found {len(sets)} sets.", level=logging.INFO)
        return sets
    
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

        
    
