.. _api-integration:

===============
API Integration
===============

Technical documentation for Inkcollector's integration with the Lorcast API and underlying implementation details.

Lorcast API Overview
===================

Inkcollector integrates with the `Lorcast API <https://api.lorcast.com>`_ to provide access to Disney Lorcana trading card data.

Base Configuration
-----------------

**Default API Settings:**

- **Base URL:** ``https://api.lorcast.com``
- **API Version:** ``v0``
- **Full Base URL:** ``https://api.lorcast.com/v0``

The API configuration is built into the application and uses these default values.

Supported Endpoints
==================

Sets Endpoint
------------

**Endpoint:** ``GET /sets``

**URL:** ``https://api.lorcast.com/v0/sets``

**Purpose:** Retrieve all available Disney Lorcana card sets.

**Response Format:**

.. code-block:: json

    {
      "results": [
        {
          "id": "TFC",
          "name": "The First Chapter",
          "code": "TFC", 
          "released_at": "2023-08-18",
          "card_count": 204
        },
        {
          "id": "ROF",
          "name": "Rise of the Floodborn",
          "code": "ROF",
          "released_at": "2023-11-17", 
          "card_count": 204
        }
      ]
    }

**Inkcollector Usage:**

.. code-block:: shell

    inkcollector lorcast get-sets

Set Detail Endpoint  
-------------------

**Endpoint:** ``GET /sets/{set_id}``

**URL:** ``https://api.lorcast.com/v0/sets/TFC``

**Purpose:** Get detailed information about a specific set.

**Response Format:**

.. code-block:: json

    {
      "id": "TFC",
      "name": "The First Chapter", 
      "code": "TFC",
      "released_at": "2023-08-18",
      "card_count": 204,
      "description": "The first set in the Disney Lorcana TCG..."
    }

**Inkcollector Usage:**

Used internally for set validation before fetching cards.

Cards Endpoint
-------------

**Endpoint:** ``GET /sets/{set_id}/cards``

**URL:** ``https://api.lorcast.com/v0/sets/TFC/cards``

**Purpose:** Retrieve all cards for a specific set.

**Response Format:**

.. code-block:: json

    {
      "results": [
        {
          "id": 1,
          "name": "Aladdin - Heroic Outlaw",
          "version": "Heroic Outlaw",
          "layout": "normal",
          "released_at": "2023-08-18",
          "image_uris": {
            "small": "https://api.lorcast.com/v0/images/small/1.jpg",
            "normal": "https://api.lorcast.com/v0/images/normal/1.jpg", 
            "large": "https://api.lorcast.com/v0/images/large/1.jpg"
          },
          "mana_cost": 2,
          "type": "Character",
          "classifications": ["Hero", "Prince"],
          "text": "...",
          "set_name": "The First Chapter",
          "set_code": "TFC",
          "set_id": "TFC",
          "rarity": "Common",
          "card_num": 1,
          "artist": "Artist Name",
          "story_setting": "Agrabah"
        }
      ]
    }

**Inkcollector Usage:**

.. code-block:: shell

    inkcollector lorcast get-cards --set-id TFC

Data Structure Details
=====================

Card Object Schema
-----------------

Each card object contains the following fields:

**Basic Information:**

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Field
     - Type
     - Description
   * - ``id``
     - ``integer``
     - Unique card identifier
   * - ``name``
     - ``string``
     - Full card name
   * - ``version``
     - ``string``
     - Card version/subtitle
   * - ``layout``
     - ``string``
     - Card layout type (usually "normal")
   * - ``released_at``
     - ``string``
     - Release date (ISO format)

**Game Mechanics:**

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Field
     - Type  
     - Description
   * - ``mana_cost``
     - ``integer``
     - Mana cost to play the card
   * - ``type``
     - ``string``
     - Card type (Character, Action, Item, etc.)
   * - ``classifications``
     - ``array``
     - List of character classifications
   * - ``text``
     - ``string``
     - Card rules text and abilities
   * - ``willpower``
     - ``integer``
     - Character willpower (if applicable)
   * - ``strength``
     - ``integer``
     - Character strength (if applicable)
   * - ``lore``
     - ``integer``
     - Lore value (if applicable)

**Set Information:**

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Field
     - Type
     - Description
   * - ``set_name``
     - ``string``
     - Name of the set
   * - ``set_code``
     - ``string``
     - Set code (TFC, ROF, etc.)
   * - ``set_id``
     - ``string``
     - Set identifier
   * - ``rarity``
     - ``string``
     - Card rarity (Common, Uncommon, Rare, etc.)
   * - ``card_num``
     - ``integer``
     - Card number within the set

**Visual Information:**

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Field
     - Type
     - Description
   * - ``image_uris``
     - ``object``
     - URLs for different image sizes
   * - ``artist``
     - ``string``
     - Card artist name
   * - ``story_setting``
     - ``string``
     - Disney story/world setting

Image URI Structure
------------------

The ``image_uris`` object provides three image sizes:

.. code-block:: json

    {
      "image_uris": {
        "small": "https://api.lorcast.com/v0/images/small/1.jpg",
        "normal": "https://api.lorcast.com/v0/images/normal/1.jpg",
        "large": "https://api.lorcast.com/v0/images/large/1.jpg"
      }
    }

**Image Sizes:**

- **small:** Thumbnail size (~150px width)
- **normal:** Standard size (~488px width) 
- **large:** High resolution (~734px width)

Implementation Details
=====================

HTTP Client Configuration
------------------------

Inkcollector uses the ``requests`` library with the following configuration:

**Timeout Settings:**

- **Connection timeout:** 10 seconds
- **Read timeout:** 30 seconds

**Headers:**

- ``User-Agent``: ``Inkcollector/1.1.0``
- ``Accept``: ``application/json``

**Example Configuration:**

.. code-block:: python

    import requests
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Inkcollector/1.1.0',
        'Accept': 'application/json'
    })
    
    response = session.get(
        'https://api.lorcast.com/v0/sets',
        timeout=(10, 30)
    )

Error Handling
-------------

Inkcollector handles various API error conditions:

**HTTP Status Codes:**

.. list-table::
   :widths: 15 25 60
   :header-rows: 1

   * - Code
     - Condition
     - Inkcollector Response
   * - 200
     - Success
     - Process data normally
   * - 404
     - Set/resource not found
     - Display helpful error message
   * - 429
     - Rate limit exceeded
     - Retry with backoff
   * - 500-599
     - Server errors
     - Retry with backoff
   * - Timeout
     - Network timeout
     - Display connectivity error

**Example Error Messages:**

.. code-block:: text

    Error: Set ID 'INVALID' not found
    - Use 'inkcollector --profile preview lorcast get-sets' to see available sets
    - Check spelling and case sensitivity

    Error: Failed to connect to Lorcast API
    - Check your internet connection
    - Verify the API is accessible: https://api.lorcast.com

Rate Limiting
------------

**Current Implementation:**

- No built-in rate limiting (API doesn't require it currently)
- Requests are made sequentially
- Natural delays from file I/O operations

**Future Considerations:**

- May add configurable delays between requests
- Potential batch processing for large collections
- Respect any future API rate limits

Data Processing
==============

JSON Processing
--------------

**Response Processing:**

1. HTTP response received from API
2. JSON parsing and validation
3. Data structure normalization
4. Optional console formatting
5. File system storage (if configured)

**File Storage Format:**

Data is stored in structured JSON files:

.. code-block:: text

    data/
    └── lorcast/
        ├── sets.json              # All sets data
        └── sets/
            ├── TFC.json           # TFC set cards
            ├── ROF.json           # ROF set cards
            └── {set_id}.json      # Other sets

**File Content Example:**

.. code-block:: json

    {
      "results": [
        {
          "id": 1,
          "name": "Aladdin - Heroic Outlaw",
          "mana_cost": 2,
          "type": "Character"
        }
      ],
      "metadata": {
        "collected_at": "2025-01-15T10:30:00Z",
        "set_id": "TFC",
        "total_cards": 204
      }
    }

Image Processing
---------------

**Download Process:**

1. Extract image URLs from card data
2. Determine target image size (small/normal/large)
3. Download images with progress tracking
4. Save with standardized naming convention
5. Report success/failure statistics

**File Naming Convention:**

.. code-block:: text

    images/
    └── lorcast/
        └── sets/
            └── {set_id}/
                ├── crd_001.jpg
                ├── crd_002.jpg
                └── crd_{card_id}.jpg

**Download Configuration:**

.. code-block:: python

    # Image download settings
    CHUNK_SIZE = 8192  # 8KB chunks
    MAX_RETRIES = 3
    RETRY_DELAY = 1.0  # seconds

Extending the Integration
========================

API Configuration
----------------

The API configuration is built into the application and uses these default endpoints:

.. code-block:: yaml

    # Built-in API configuration (not user-configurable):
    # api_base_url: https://api.lorcast.com
    # api_version: v0

Adding New Endpoints
-------------------

If the Lorcast API adds new endpoints, Inkcollector can be extended:

**Example: Hypothetical deck endpoint**

.. code-block:: python

    # Future implementation example
    def get_deck_info(deck_id):
        """Get deck information from API."""
        url = f"https://api.lorcast.com/v0/decks/{deck_id}"
        response = session.get(url, timeout=(10, 30))
        return response.json()

Integration Best Practices
==========================

API Usage Guidelines
-------------------

**Be Respectful:**

- Don't make excessive concurrent requests
- Add delays for large batch operations
- Cache responses when appropriate
- Use appropriate timeout values

**Error Handling:**

- Always check HTTP status codes
- Implement retry logic for transient failures
- Provide helpful error messages to users
- Log errors for debugging

**Data Management:**

- Store responses in structured formats
- Use consistent naming conventions
- Implement data validation
- Consider data freshness and updates

Example Integration Code
-----------------------

**Basic API Client:**

.. code-block:: python

    import requests
    import time
    from pathlib import Path

    class LorcastClient:
        def __init__(self, base_url="https://api.lorcast.com", version="v0"):
            self.base_url = f"{base_url}/{version}"
            self.session = requests.Session()
            self.session.headers.update({
                'User-Agent': 'Inkcollector/1.1.0',
                'Accept': 'application/json'
            })
        
        def get_sets(self):
            """Get all card sets."""
            response = self.session.get(
                f"{self.base_url}/sets",
                timeout=(10, 30)
            )
            response.raise_for_status()
            return response.json()
        
        def get_cards(self, set_id):
            """Get cards for a specific set."""
            response = self.session.get(
                f"{self.base_url}/sets/{set_id}/cards",
                timeout=(10, 30)
            )
            response.raise_for_status()
            return response.json()
        
        def download_image(self, url, output_path):
            """Download a card image."""
            response = self.session.get(url, stream=True, timeout=(10, 30))
            response.raise_for_status()
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

**Usage Example:**

.. code-block:: python

    # Initialize client
    client = LorcastClient()
    
    # Get all sets
    sets_data = client.get_sets()
    print(f"Found {len(sets_data['results'])} sets")
    
    # Get cards for first set
    first_set = sets_data['results'][0]
    cards_data = client.get_cards(first_set['id'])
    print(f"Found {len(cards_data['results'])} cards")
    
    # Download first card image
    first_card = cards_data['results'][0]
    image_url = first_card['image_uris']['normal']
    output_path = Path(f"images/{first_card['id']}.jpg")
    client.download_image(image_url, output_path)

Future API Enhancements
======================

Potential Additions
------------------

**Caching Layer:**

- Local caching of API responses
- Configurable cache expiration
- Cache invalidation strategies

**Batch Operations:**

- Bulk card requests
- Parallel image downloads
- Progress reporting

**API Monitoring:**

- Response time tracking
- Error rate monitoring
- API health checks

**Advanced Filtering:**

- Server-side filtering options
- Custom query parameters
- Pagination support

Contributing to API Integration
==============================

If you want to contribute to the API integration:

1. **Test thoroughly** with different API responses
2. **Handle edge cases** gracefully
3. **Add comprehensive error handling**
4. **Document new features** clearly
5. **Follow existing patterns** and conventions

**Development Setup:**

.. code-block:: shell

    # Clone and set up development environment
    git clone https://github.com/bertcafecito/inkcollector.git
    cd inkcollector
    python -m venv venv
    source venv/bin/activate  # or venv\Scripts\activate on Windows
    pip install -e ".[dev]"

Next Steps
==========

- Learn about :doc:`troubleshooting` API-related issues
- Check :doc:`examples` for advanced API usage patterns
- See :doc:`cli-reference` for complete command documentation
