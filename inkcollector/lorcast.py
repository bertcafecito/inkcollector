import logging
import os
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
        self.api_current_version = "v0"
        self.api_rate_limit = 5 # delay per request in seconds
        self.api_url = f"{self.api_base_url}/{self.api_current_version}"
        super().__init__(name=self.name)

        # Set up directories with name
        self.data_dir = f"{self.data_dir}/{self.name}"
        self.images_dir = f"{self.images_dir}/{self.name}"

        self.setup_directories(self.data_dir)
        self.setup_directories(self.images_dir)

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
    
    def get_cards(self, set_id, download_images=False):
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

        if download_images:
            # Create set directory if it does not exist
            set_dir = f"{self.images_dir}/{set_id}"
            self.setup_directories(set_dir)
            
            for card in cards:
                image_uri = card.get("image_uris").get("digital").get("large")

                if image_uri:
                    self.download_card_images(image_uri, set_dir)
                    
        
        self.log(f"Found {len(cards)} cards.", level=logging.INFO)
        return cards
    
    def download_card_images(self, image_uri, set_dir):
        """
        Download the card images from the provided URI.
        
        Args:
            image_uri (str): The URI of the card image to download.
            set_dir (str): The directory to save the downloaded image.
        """

        try:
            response = requests.get(image_uri)
            response.raise_for_status()  # Raise an error for bad responses
        except requests.exceptions.RequestException as e:
            self.log(f"Error downloading image: {str(e)}", level=logging.ERROR)
            return None
        
        if response.status_code == 200:
            file_name = os.path.basename(image_uri)
            # Remove query parameters from the file name
            if "?" in file_name:
                file_name = file_name.split("?")[0]
                self.log("Removed query parameters from file name", level=logging.INFO)
            file_path = os.path.join(set_dir, file_name)
            image_data = response.content
        else:
            self.log(f"Response Error: {response.status_code} - {response.text}", level=logging.ERROR)
            return None
        
        with open(file_path, "wb") as image_file:
            image_file.write(image_data)
    
        self.log(f"Downloaded image for {file_name}.", level=logging.INFO)
        return None
        

    
    
