"""
Module for representing a travel path between two destinations.

Defines the Path class that retrieves travel information using an external API,
and a dummyPath class for testing or simplified use cases.
"""

from model.APIs.googleAPI import getInfo

class Path:
    """Represents a travel path between two locations using the Google Maps API."""

    def __init__(self, d1, d2):
        """Initialize a Path instance.

        Args:
            d1 (str): The origin location.
            d2 (str): The destination location.
        """
        self.start = d1
        self.end = d2
        # Retrieve travel information from the external API.
        time, text = getInfo(d1, d2)
        self.time_num = time  # Numeric travel time used for computation.
        self.time_str = text  # Human-readable travel time.
        self.POI = []         # List to store points of interest along the route.

class dummyPath:
    """Represents a dummy travel path with a predefined travel time for testing purposes."""

    def __init__(self, d1, d2, time):
        """Initialize a dummyPath instance.

        Args:
            d1 (str): The origin location.
            d2 (str): The destination location.
            time (int): Predefined travel time in seconds.
        """
        self.start = d1
        self.end = d2
        self.time_num = time
        self.POI = []
