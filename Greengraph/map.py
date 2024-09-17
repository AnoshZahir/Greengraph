"""
This module defines the Map class, which is used to interact with the Google Maps API
to retrieve static satellite images, analyze the greenness of a map, and count the 
number of green pixels.

The Map class provides methods to:
- Fetch a static satellite image from Google Maps for a specific location.
- Analyze the pixel data of the image to determine which pixels are green.
- Count the total number of green pixels in the image.
- Generate a new image highlighting the green pixels.

Dependencies:
- numpy
- requests
- matplotlib
"""

import numpy as np
from io import StringIO
from matplotlib import image as img
import requests
from typing import Tuple

class Map(object):
    def __init__(self, lat: float, long: float, satellite: bool = True, zoom: int = 10, size: Tuple[int, int] = (400, 400), sensor: bool = False):
        """
        Initialize a Map object with the provided latitude, longitude, and other optional parameters.
        
        Args:
            lat (float): Latitude of the location.
            long (float): Longitude of the location.
            satellite (bool): Whether to use satellite imagery. Default is True.
            zoom (int): Zoom level of the map. Default is 10.
            size (Tuple[int, int]): Size of the map image in pixels. Default is (400, 400).
            sensor (bool): Whether the map is based on a sensor. Default is False.
        """

        base = "http://maps.googleapis.com/maps/api/staticmap?"
        
        params = dict(
              sensor = str(sensor).lower(),
              zoom = zoom, 
              size = "x".join(map(str, size)),
              center = ",".join(map(str, (lat, long))),
              style = "feature:all|element:labels|visibility:off"
              )
        if satellite:
            params["maptype"] = "satellite"
        
        self.image = requests.get(base, params = params).content #response.get returns a 'Response' object.
        self.pixels = img.imread(StringIO(self.image))
    
    def green(self, threshold: float) -> np.ndarray:
        """
        Determine which pixels are green based on the threshold value.

        Args:
            threshold (float): Threshold to determine greenness of a pixel.

        Returns:
            np.ndarray: A 2D array of boolean values indicating whether each pixel is green.
        """
        greener_than_red = self.pixels[:, :, 1] > threshold * self.pixels[:, :, 0]
        greener_than_blue = self.pixels[:, :, 1] > threshold * self.pixels[:, :, 2]
        green = np.logical_and(greener_than_red, greener_than_blue)
        return green # 400x400 array of true/false values. 
    
    def count_green(self, threshold:float = 1.1) -> int:
        """
        Count the number of green pixels in the image based on the threshold value.

        Args:
            threshold (float): Threshold to determine greenness of a pixel. Default is 1.1.

        Returns:
            int: Total number of green pixels.
        """
        return np.sum(self.green(threshold))
    
    def show_green(self, threshold:float = 1.1) -> bytes:
        """
        Generate an image where green pixels are highlighted.

        Args:
            threshold (float): Threshold to determine greenness of a pixel. Default is 1.1.

        Returns:
            bytes: The binary content of the generated image.
        """
        green = self.green(threshold) # return an array of true/false 
        out = green[:, :, np.newaxis] * np.array([0, 1, 0])[np.newaxis, np.newaxis, :]
        buffer = StringIO()
        img.imsave(buffer, out, format = 'png')
        return buffer.getvalue()