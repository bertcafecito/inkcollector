import json

import requests


class LorcastAPI:
    """
    A class to interact with the Lorcast API for collecting data on the
    Lorcana Trading Card Game.

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
        self.session.headers.update(
            {
                "User-Agent": "InkCollector/1.0.0",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

    def get_sets(self):
        """
        Retrieves a list of all sets available in the Lorcast API.

        Returns:
            list: A list of sets, each represented as a dictionary with set details.
        """
        url = f"{self.api_url}/sets"

        try:
            response = self.session.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes

            return response.json().get("results", [])
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            raise
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON response: {e}")
            raise ValueError(f"Invalid JSON response: {e}")

    def get_set(self, set_id):
        """
        Retrieves details of a specific set from the Lorcast API.

        Parameters:
            set_id (str): The ID of the set to retrieve.

        Returns:
            dict: A dictionary containing details of the specified set.
        """
        url = f"{self.api_url}/sets/{set_id}"

        # Check if set_id is provided
        if not set_id:
            raise ValueError("set_id must be provided to fetch set details.")

        try:
            response = self.session.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes

            return response.json()
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            raise
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON response: {e}")
            raise ValueError(f"Invalid JSON response: {e}")

    def get_cards(self, set_id):
        """
        Retrieves a list of cards for a specific set from the Lorcast API.

        Parameters:
            set_id (str): The ID of the set to retrieve cards for.

        Returns:
            list: A list of cards in the specified set, each represented as a
                dictionary with card details.
        """
        url = f"{self.api_url}/sets/{set_id}/cards"

        # Check if set_id is provided
        if not set_id:
            raise ValueError("set_id must be provided to fetch cards.")

        try:
            response = self.session.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes

            return response.json()
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            raise
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON response: {e}")
            raise ValueError(f"Invalid JSON response: {e}")

    def download_image(self, image_url, output_path):
        """
        Downloads an image from the specified URL and saves it to the given output path.

        Parameters:
            image_url (str): The URL of the image to download.
            output_path (str): The file path where the image will be saved.
        """
        try:
            response = self.session.get(image_url, stream=True)
            response.raise_for_status()  # Raise an exception for bad status codes

            with open(output_path, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Image downloaded and saved to {output_path}")
        except requests.RequestException as e:
            print(f"Failed to download image: {e}")
            raise
        except IOError as e:
            print(f"Failed to save image to {output_path}: {e}")
            raise
