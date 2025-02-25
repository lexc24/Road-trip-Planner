"""
Module for interacting with the Google Maps API to retrieve travel information.

This module initializes a Google Maps client and provides the getInfo function,
which retrieves travel durations between two locations.
"""

import googlemaps

Maps = googlemaps.Client(key="AIzaSyDsot6rPPwovlqUfo8-TGyF1KNSfG1D9e4")


def getInfo(start, end):
    """
    Retrieve travel time information between two locations using the Google Maps Directions API.

    Args:
        start (str): The starting location (address or place name).
        end (str): The destination location (address or place name).

    Returns:
        tuple: A tuple containing:
            - duration_num (int): The travel duration in seconds.
            - duration_str (str): The travel duration as a human-readable string.
    """
    # Request driving directions with imperial units.
    results = Maps.directions(start, end, mode="driving", units="imperial")
    # Extract numeric duration (in seconds) from the first leg of the first route.
    duration_num = results[0]['legs'][0]['duration']['value']
    # Extract human-readable duration from the same leg.
    duration_str = results[0]['legs'][0]['duration']['text']
    return duration_num, duration_str
