""""
This module contains the Greengraph class, which includes methods for geolocation,
generating location sequences, and analyzing green space between two specified locations.
"""

import numpy as np
import geopy
from Greengraph.map import Map
from typing import Optional

class Greengraph(object):
    """
    A class to analyze green space between two specified locations using satellite imagery.

    Attributes:
        start (str): The starting location for the analysis.
        end (str): The ending location for the analysis.
        geocoder (object): Optional geocoder instance. Defaults to GoogleV3 geocoder if not provided.
    """
    
    def __init__(self, start: str, end: str, geocoder=None):
        """
        Instantiate a Greengraph object with the specified start and end locations.
        
        Args:
            start (str): The starting location for the analysis.
            end (str): The ending location for the analysis.
            geocoder (object): An optional geocoder instance for geolocation. Defaults to GoogleV3 geocoder.
        """
        self.start = start
        self.end = end
        self.geocoder = geocoder or geopy.geocoders.GoogleV3(domain = "maps.google.co.uk")
    
    def geolocate(self, place:str) -> Optional[tuple]:
        """
        Return the latitude and longitude of the specified location.

        Args:
            place (str): The location to geolocate.

        Returns:
            tuple: A tuple containing the latitude and longitude of the location, or None if not found.
        """

        geocode_result = self.geocoder.geocode(place, exactly_one=False)
        return geocode_result[0][1] if geocode_result else None
        
    def location_sequence(self, start:tuple, end:tuple, steps:int) -> np.ndarray:
        """
        Generate evenly spaced coordinates between the start and end locations.

        Args:
            start (tuple): The starting coordinates (latitude, longitude).
            end (tuple): The ending coordinates (latitude, longitude).
            steps (int): The number of intervals between the start and end locations.

        Returns:
            np.ndarray: An array of coordinates between the start and end locations.
        """
        lats = np.linspace(start[0], end[0], steps)
        longs = np.linspace(start[1], end[1], steps)
        return np.vstack([lats, longs]).transpose()
    
    def green_between(self, steps:int) -> list:
        """
        Calculate the number of green pixels at each interval between two locations.

        Args:
            steps (int): The number of intervals between the start and end locations.

        Returns:
            list: A list of the number of green pixels at each interval, or an empty list if locations are invalid.
        """
        start_coords = self.geolocate(self.start)
        end_coords = self.geolocate(self.end)

        # Error handling for the case when the geolocate method returns None.
        if start_coords is None or end_coords is None:
            return []
        
        return [Map(*location).count_green()
            for location in self.location_sequence(start_coords, end_coords, steps)]