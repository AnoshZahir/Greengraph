from ..graph import Greengraph
from ..map import Map

import requests
import numpy as np
import matplotlib

import os
import yaml

from nose.tools import assert_called_with, assert_equal
from mock import patch

@patch.object(requests, 'get')
@patch.object(matplotlib.image, 'imread')
def test_build_default_params(mock_imread, mock_get):    
    
    with open(os.path.join(os.path.dirname(__file__),'data','map_data.yaml')) as dataset:
        map_data = yaml.load(dataset)['test_map']
        
        for data in map_data:
            test = data.pop('test')
            url = data.pop('url')
            latitude = data.pop('latitude')
            longitude = data.pop('longitude')
            params = data.pop('params')
            if (test == 'default'):
                actual_map = Map(latitude,longitude)
            elif (test == 'satellite_false'):
                actual_map = Map(latitude,longitude,satellite = False)
            elif (test == 'zoom'):
                actual_map = Map(latitude,longitude,zoom = 30)
            elif (test == 'size'):
                actual_map = Map(latitude,longitude,size = (300,300))
            elif (test == 'sensor_true'): 
                actual_map = Map(latitude,longitude,sensor = True)
            
            mock_get.assert_called_with(url,params=params)

@patch.object(requests, 'get')
@patch(matplotlib.image, 'imread')
#@patch.object(Map, 'green')
def test_green(mock_imread, mock_get):
    '''
    Test that the function can take a 3d matrix, and return a matrix of true/false values.
    Data is taken from the 'test_green' subsection of map_data.yaml.
    '''
    my_map = Map(51.50, -0.12)
    
    with open(os.path.join(os.path.dirname(__file__), 'data', 'map_data.yaml')) as dataset:
        map_data = yaml.load(dataset)['test_green']
    
    for data in map_data:
        threshold = data.pop('test')
        input_matrix = data.pop('3d_input_matrix')
        expected_return = data.pop('2d_output_matrix')
        my_map.__setattr__('pixels', input_matrix)
        actual_return = my_map.green(threshold)
        assert_equal(expected_return, actual_return)

@patch.object(Map, 'green')
def test_count_green(mock_green):
    '''
    Test that a 2d input matrix of true/false values is correctly summed. 
    Data is taken from the 'test_count_green' subsection of map_data.yaml.
    '''
    my_map = Map(51.50, -0.12)

    with open(os.path.join(os.path.dirname(__file__), 'data', 'map_data.yaml')) as dataset:
        map_data = yaml.load(dataset)['test_count_green']
    
    for data in map_data:
        input_values = data.pop('input_values')
        expected_return = data.pop('result')
        
        mock_green.return_value = input_values
        actual_return = my_map.count_green() #threshold kept unchanged for this test.
        assert_equal(actual_return, expected_return)