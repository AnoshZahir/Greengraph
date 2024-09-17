"""
Unit tests for the Map class and its interactions with the Greengraph class.
This file includes tests for building map parameters, green pixel calculations,
and counting green pixels between two locations.
"""

from ..graph import Greengraph
from ..map import Map

import requests
import numpy as np
import matplotlib

import os
import yaml

import unittest
from unittest.mock import patch

@patch.object(requests, 'get')
@patch.object(matplotlib.image, 'imread')
def test_build_default_params(mock_imread, mock_get):    
    """
    Test that the URL parameters for the Map class are built correctly 
    based on different input arguments (satellite, zoom, size, sensor).
    Mocks 'requests.get' and 'matplotlib.image.imread' to avoid actual API calls.
    """  
    with open(os.path.join(os.path.dirname(__file__),'data','map_data.yaml')) as dataset:
        map_data = yaml.load(dataset, Loader=yaml.SafeLoader)['test_map'] # Use SafeLoader for YAML
        
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
@patch(matplotlib.image, 'imread')
def test_green(mock_imread, mock_get):
    """
    Test that the 'green' method returns a matrix of True/False values based on 
    whether the pixels are classified as green, using different thresholds.
    Mocks 'requests.get' and 'matplotlib.image.imread' to avoid actual image loading.
    """
    my_map = Map(51.50, -0.12)
    
    with open(os.path.join(os.path.dirname(__file__), 'data', 'map_data.yaml')) as dataset:
        map_data = yaml.load(dataset, Loader=yaml.SafeLoader)['test_green']
    
    for data in map_data:
        threshold = data.pop('test')
        input_matrix = data.pop('3d_input_matrix')
        expected_return = data.pop('2d_output_matrix')
        my_map.__setattr__('pixels', input_matrix) # Injecting mock pixel data
        actual_return = my_map.green(threshold)
        assert_equal(expected_return, actual_return)

@patch.object(Map, 'green')
def test_count_green(mock_green):
    """
    Test that the 'count_green' method accurately sums the True/False values 
    representing green pixels.
    Data is taken from the 'test_count_green' subsection of map_data.yaml.
    """
    my_map = Map(51.50, -0.12)

    with open(os.path.join(os.path.dirname(__file__), 'data', 'map_data.yaml')) as dataset:
        map_data = yaml.load(dataset, Loader=yaml.SafeLoader)['test_count_green']
    
    for data in map_data:
        input_values = data.pop('input_values')
        expected_return = data.pop('result')
        
        mock_green.return_value = input_values # Mocking the green pixel data
        actual_return = my_map.count_green() # Count green pixels
        assert_equal(actual_return, expected_return)