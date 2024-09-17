"""
Unit tests for the Map class and its interactions with the Greengraph class.
This file includes tests for building map parameters, green pixel calculations,
and counting green pixels between two locations.
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

    @patch.object(requests, 'get')
    @patch('matplotlib.image.imread')
    def test_build_default_params(self, mock_imread, mock_get):    
        """
        Test that the URL parameters for the Map class are built correctly 
        based on different input arguments (satellite, zoom, size, sensor).
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
        Test that the 'green' method returns a matrix of True/False values based on 
        whether the pixels are classified as green.
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

            my_map.pixels = input_matrix  # Injecting mock pixel data
            actual_return = my_map.green(threshold)
            
            np.testing.assert_array_equal(expected_return, actual_return)

    @patch.object(Map, 'green')
    @patch('matplotlib.image.imread')
    def test_count_green(self, mock_imread, mock_green):
        """
        Test that the 'count_green' method accurately sums the True/False values 
        representing green pixels.
        """
        mock_imread.return_value = np.random.rand(400, 400, 3).astype(np.float32)
        mock_green.return_value = np.array([[True, False], [True, True]])

        my_map = Map(51.50, -0.12)
        result = my_map.count_green()

        self.assertEqual(result, 3)

        #with open(os.path.join(os.path.dirname(__file__), 'data', 'map_data.yaml')) as dataset:
        #    map_data = yaml.load(dataset, Loader=yaml.SafeLoader)['test_count_green']
        
        #for data in map_data:
         #   input_values = data.pop('input_values')
         #   expected_return = data.pop('result')
            
            # Mocking the green pixel data
         #   mock_green.return_value = input_values
         #   actual_return = my_map.count_green()

         #   self.assertEqual(actual_return, expected_return)

if __name__ == '__main__':
    unittest.main()