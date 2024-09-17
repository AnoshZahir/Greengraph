"""
Unit tests for the `Map` class and its interactions with the `Greengraph` class.

This module includes tests to validate the following functionality:
- URL parameter construction based on user inputs.
- Calculation of green pixels based on satellite image data.
- Counting the number of green pixels for specified locations.
- Simulating image retrieval and processing from the Google Maps API.

The tests use mocking to avoid actual HTTP requests and image processing while ensuring that the
core functionality of the `Map` class operates as expected.
"""

from Greengraph.graph import Greengraph
from Greengraph.map import Map

import requests
import numpy as np
import matplotlib

import os
import yaml

import unittest
from unittest.mock import patch

class TestMap(unittest.TestCase):
    """
    Unit tests for the `Map` class to validate:
    - URL parameter construction.
    - Green pixel calculation.
    - Green pixel counting.
    
    Mocks external dependencies like `requests` and `matplotlib` to focus on internal logic.
    """

    @patch.object(requests, 'get')
    @patch('matplotlib.image.imread')
    def test_build_default_params(self, mock_imread, mock_get):    
        """
        Test URL parameter construction for the `Map` class.

        Ensures that different input combinations for satellite imagery, zoom, size, and sensor
        options correctly build the expected URL parameters for the Google Maps API.
        """
        # Mock the image response to be a valid 400x400x3 NumPy array
        mock_imread.return_value = np.random.rand(400, 400, 3).astype(np.float32)
        mock_get.return_value.content = b"mock_image_data"

        with open(os.path.join(os.path.dirname(__file__),'data','map_data.yaml')) as dataset:
            map_data = yaml.safe_load(dataset)['test_map'] # Use SafeLoader for YAML
            
            for data in map_data:
                test = data.pop('test')
                url = data.pop('url')
                latitude = data.pop('latitude')
                longitude = data.pop('longitude')
                params = data.pop('params')

                # Testing different input cases for the Map class
                if (test == 'default'):
                    actual_map = Map(latitude,longitude)
                elif (test == 'satellite_false'):
                    actual_map = Map(latitude,longitude,satellite=False)
                elif (test == 'zoom'):
                    actual_map = Map(latitude,longitude,zoom=30)
                elif (test == 'size'):
                    actual_map = Map(latitude,longitude,size=(300,300))
                elif (test == 'sensor_true'): 
                    actual_map = Map(latitude,longitude,sensor=True)
                
                mock_get.assert_called_with(url,params=params)

    @patch.object(requests, 'get')
    @patch('matplotlib.image.imread')
    def test_green(self, mock_imread, mock_get):
        """
        Test the `green` method to verify correct identification of green pixels.

        This test ensures that the method correctly returns a boolean matrix where `True`
        values correspond to pixels classified as green based on the input threshold.
        """
        # Mock the image response to be a valid 400x400x3 NumPy array
        mock_imread.return_value = np.random.rand(400, 400, 3).astype(np.float32)
        mock_get.return_value.content = b"mock_image_data"

        my_map = Map(51.50, -0.12)
        
        with open(os.path.join(os.path.dirname(__file__), 'data', 'map_data.yaml')) as dataset:
            map_data = yaml.safe_load(dataset)['test_green']

        for data in map_data:
            threshold = float(data.pop('test'))
            input_matrix = np.array(data.pop('3d_input_matrix')).astype(np.float32)
            expected_return = np.array(data.pop('2d_output_matrix')).astype(bool)

            my_map.pixels = input_matrix  # Inject mock pixel data
            actual_return = my_map.green(threshold)
            
            np.testing.assert_array_equal(expected_return, actual_return)

    @patch.object(Map, 'green')
    @patch('matplotlib.image.imread')
    def test_count_green(self, mock_imread, mock_green):
        """
        Test the `count_green` method to verify correct counting of green pixels.

        This test ensures that the method returns the correct number of green pixels
        when provided with a mocked green pixel matrix.
        """
        # Mock image and green pixel data
        mock_imread.return_value = np.random.rand(400, 400, 3).astype(np.float32)
        mock_green.return_value = np.array([[True, False], [True, True]])

        my_map = Map(51.50, -0.12)
        result = my_map.count_green()

        self.assertEqual(result, 3)

if __name__ == '__main__':
    unittest.main()