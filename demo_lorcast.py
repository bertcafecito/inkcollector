"""
Demo script showing how to get data from the LorCast API.

Quick Usage Example:
    from demo_lorcast import LorCastAPI
    
    # Basic usage
    api = LorCastAPI()
    sets_data = api.get_sets()
    print(sets_data)
    
    # Using context manager (recommended)
    with LorCastAPI() as api:
        sets = api.get_sets()
        set_names = api.get_set_names()
        legends_sets = api.search_sets_by_name("Legends")
"""
import requests
import json
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin


class LorCastAPI:
    """
    A class to interact with the LorCast API.
    
    This class provides methods to fetch data from the LorCast API endpoints,
    specifically focusing on the /v0/sets endpoint.
    """
    
    def __init__(self, base_url: str = "https://api.lorcast.com/"):
        """
        Initialize the LorCast API client.
        
        Args:
            base_url (str): The base URL for the LorCast API. Defaults to "https://api.lorcast.com/"
        """
        self.base_url = base_url.rstrip('/') + '/'
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            'User-Agent': 'InkCollector/1.0.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
    
    def _make_request(self, endpoint: str, method: str = 'GET', params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make a request to the LorCast API.
        
        Args:
            endpoint (str): The API endpoint to call
            method (str): HTTP method to use (GET, POST, etc.)
            params (dict, optional): Query parameters to include in the request
            
        Returns:
            dict: The JSON response from the API
            
        Raises:
            requests.RequestException: If the request fails
            ValueError: If the response is not valid JSON
        """
        url = urljoin(self.base_url, endpoint)
        
        try:
            response = self.session.request(method, url, params=params)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            return response.json()
            
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            raise
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON response: {e}")
            raise ValueError(f"Invalid JSON response: {e}")
    
    def get_sets(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Get sets data from the LorCast API.
        
        Args:
            params (dict, optional): Query parameters to filter the results
            
        Returns:
            dict: The sets data from the API
            
        Example:
            >>> api = LorCastAPI()
            >>> sets = api.get_sets()
            >>> print(f"Found {len(sets.get('data', []))} sets")
        """
        return self._make_request('v0/sets', params=params)
    
    def get_sets_with_filters(self, 
                             name: Optional[str] = None,
                             code: Optional[str] = None,
                             limit: Optional[int] = None) -> Dict[str, Any]:
        """
        Get sets data with common filters.
        
        Args:
            name (str, optional): Filter by set name
            code (str, optional): Filter by set code
            limit (int, optional): Limit the number of results
            
        Returns:
            dict: The filtered sets data from the API
        """
        params = {}
        
        if name:
            params['name'] = name
        if code:
            params['code'] = code
        if limit:
            params['limit'] = limit
            
        return self.get_sets(params)
    
    def get_set_names(self) -> List[str]:
        """
        Get a list of all set names.
        
        Returns:
            list: A list of set names
        """
        sets_data = self.get_sets()
        sets_list = sets_data.get('results', sets_data.get('data', []))
        
        return [set_info.get('name', '') for set_info in sets_list if set_info.get('name')]
    
    def get_set_codes(self) -> List[str]:
        """
        Get a list of all set codes.
        
        Returns:
            list: A list of set codes
        """
        sets_data = self.get_sets()
        sets_list = sets_data.get('results', sets_data.get('data', []))
        
        return [set_info.get('code', '') for set_info in sets_list if set_info.get('code')]
    
    def search_sets_by_name(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Search for sets by name (case-insensitive).
        
        Args:
            search_term (str): The term to search for in set names
            
        Returns:
            list: A list of sets matching the search term
        """
        sets_data = self.get_sets()
        sets_list = sets_data.get('results', sets_data.get('data', []))
        
        search_term_lower = search_term.lower()
        matching_sets = []
        
        for set_info in sets_list:
            set_name = set_info.get('name', '')
            if search_term_lower in set_name.lower():
                matching_sets.append(set_info)
                
        return matching_sets
    
    def close(self):
        """Close the session."""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


def demo():
    """
    Demonstration function showing how to use the LorCastAPI class.
    """
    print("LorCast API Demo")
    print("=" * 50)
    
    # Create an instance of the API client
    with LorCastAPI() as api:
        try:
            # Get all sets
            print("1. Fetching all sets...")
            sets_data = api.get_sets()
            print(f"   Response type: {type(sets_data)}")
            
            # Handle both 'results' and 'data' keys for flexibility
            sets_list = sets_data.get('results', sets_data.get('data', []))
            
            if sets_list:
                sets_count = len(sets_list)
                print(f"   Found {sets_count} sets")
                
                # Show first few sets
                if sets_count > 0:
                    print("\n2. First 3 sets:")
                    for i, set_info in enumerate(sets_list[:3]):
                        print(f"   {i+1}. {set_info.get('name', 'Unknown')} ({set_info.get('code', 'Unknown')})")
                
                # Get set names
                print("\n3. Getting all set names...")
                set_names = api.get_set_names()
                print(f"   Found {len(set_names)} set names")
                if set_names:
                    print(f"   First 5 names: {set_names[:5]}")
                
                # Get set codes
                print("\n4. Getting all set codes...")
                set_codes = api.get_set_codes()
                print(f"   Found {len(set_codes)} set codes")
                if set_codes:
                    print(f"   First 5 codes: {set_codes[:5]}")
                
                # Search for sets containing "Legends"
                print("\n5. Searching for sets containing 'Legends'...")
                legends_sets = api.search_sets_by_name("Legends")
                print(f"   Found {len(legends_sets)} sets with 'Legends' in the name")
                for set_info in legends_sets:
                    print(f"   - {set_info.get('name', 'Unknown')}")
                
                # Example with filters
                print("\n6. Getting sets with limit of 5...")
                limited_sets = api.get_sets_with_filters(limit=5)
                limited_list = limited_sets.get('results', limited_sets.get('data', []))
                if limited_list:
                    print(f"   Retrieved {len(limited_list)} sets")
            else:
                print("   No sets found in response")
                print(f"   Response keys: {list(sets_data.keys())}")
                print(f"   Full response: {sets_data}")
            
        except Exception as e:
            print(f"Error occurred: {e}")
            print(f"Error type: {type(e).__name__}")


if __name__ == "__main__":
    demo()
