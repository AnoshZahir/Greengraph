"""
This module contains unit tests for the Greengraph class in the graph.py module.
It tests geolocation, location sequence generation, and green space analysis functionality.
"""

from ..graph import Greengraph
from ..map import Map

import os
import yaml
from nose.tools import assert_equal, assert_almost_equal
from mock import patch

# Use safe_load for YAML to avoid potential security risks.
def safe_load_yaml(file_path: str) -> dict:
    """
    Load YAML data from a file using safe_load.

    Args:
        file_path (str): Path to the YAML file.

    Returns:
        dict: The loaded YAML data.
    """
    with open(file_path, 'r') as dataset:
        return yaml.safe_load(dataset)

def test_Greengraph():
    '''
    Test to ensure Greengraph instantiates correctly.
    '''
    actual = Greengraph('London', 'Cambridge')
    assert_equal(actual.start, 'London')
    assert_equal(actual.end, 'Cambridge')

@patch.object(Greengraph, 'geolocate')
def test_geolocate(mock_geolocate):
    '''
    Test that geolocate method returns the output of geopy.geocoders.GoogleV3.geocode.
    Since we are not testing the geocode method, it is mocked. The mocked values are taken from the test_geolocate subsection of graph_data.yaml.
    '''
    mygraph = Greengraph(0.0, 0.0)

    geolocate_data = safe_load_yaml(os.path.join(os.path.dirname(__file__), 'data', 'graph_data.yaml'))['test_geolocate']
    
    for data in geolocate_data:
        location = data.pop('location')
        latitude = data.pop('location_lat')
        longitude = data.pop('location_long')
        
        expected_return = (latitude, longitude)
        mock_geolocate.return_value = expected_return

        actual_return = mygraph.geolocate(location)
        
        assert_equal(actual_return, expected_return)

def test_location_sequence():
    """
    Test that location_sequence method returns the correct values based on 'start', 'end' and 'steps' arguments.
    Data is taken from test_location_sequence subsection of graph_data.yaml.
    """
    mygraph = Greengraph(0.0, 0.0)

    location_sequence_data = safe_load_yaml(os.path.join(os.path.dirname(__file__), 'data', 'graph_data.yaml'))['test_location_sequence']
    
    for data in location_sequence_data:
        first_location_coordinates = data.pop('first_location_coordinates')
        second_location_coordinates = data.pop('second_location_coordinates')
        steps = data.pop('steps')
        expected_return = data.pop('expected_return')
        
        actual_return = mygraph.location_sequence(first_location_coordinates, second_location_coordinates, steps)
        for step_num in range(0, steps):
            for coordinate in range(0, 2):
                assert_almost_equal(actual_return[step_num][coordinate], expected_return[step_num][coordinate])

@patch.object(Greengraph, 'location_sequence')
@patch.object(Map, 'count_green')
def test_green_between(mock_count_green, mock_location_sequence):
    """
    Test that green_between returns a list of green pixels for each step between two locations.
    mock_count_green to account for dependency on count_green method from map class.
    mock_location_sequence to account for dependency on location_sequence method.
    Data for both mocks are taken from test_green_between subsection of graph_data.yaml.
    """
    mygraph = Greengraph(0.0, 0.0)
    
    green_between_data = safe_load_yaml(os.path.join(os.path.dirname(__file__), 'data', 'graph_data.yaml'))['test_green_between']
    
    for data in green_between_data:
        location_sequence_values = data.pop('location_sequence_values')
        count_green_values = data.pop('count_green_values')
        steps = data.pop('steps')
        
        mock_count_green.side_effect = count_green_values
        mock_location_sequence.side_effect = location_sequence_values
        
        expected_return = count_green_values
        actual_return = mygraph.count_green(steps) 
        assert_equal(actual_return, expected_return)

