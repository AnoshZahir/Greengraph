from ..graph import Greengraph
from ..map import Map

import geopy
import requests
import numpy as np
from matplotlib import image as img

import os
import yaml

from nose.tools import assert_equal, assert_almost_equal
from mock import patch, Mock

def test_Greengraph():
    '''
    Test to ensure Greengraph instantiates correctly.
    '''
    actual = Greengraph('London', 'Cambridge')
    assert_equal(actual.start, 'London')
    assert_equal(actual.end, 'Cambridge')

@patch.object(geopy.geocoders.GoogleV3, 'geocode')
def test_geolocate(mock_geocoder):
    '''
    Test that geolocate method returns the correct latitude and longitude values for given locations.
    '''
    mygraph = Greengraph(0.0, 0.0)
    
    with open(os.path.join(os.path.dirname(__file__), 'data', 'graph_data.yaml')) as dataset:
        geolocate_data = yaml.load(dataset)['test_geolocate']
    
    for data in geolocate_data:
        location = data.pop('location')
        latitude = data.pop('location_lat')
        longitude = data.pop('location_long')
        mock_geocoder.asser_equal(mygraph.geolocate(location), (latitude, longitude))
    
def test_location_sequence():
    '''
    Test that location_sequence method returns the correct values based on
    numbers given in the method's 'start', 'end' and 'steps' arguments. 
    '''
    mygraph = Greengraph(0.0, 0.0)
    
    with open(os.path.join(os.path.dirname(__file__), 'data', 'graph_data.yaml')) as dataset:
        location_sequence_data = yaml.load(dataset)['test_location_sequence']
    
    for data in location_sequence_data:
        first_location = data.pop('first_location')
        second_location = data.pop('second_location')
        steps = data.pop('steps')
        sequence_results = data.pop('sequence_results')
        actual_results = mygraph.location_sequence(mygraph.geolocate(first_location), mygraph.geolocate(second_location), steps)
        for step_location in range(0, len(actual_results)):
            for location_coordinate in range(0, len(actual_results[step_location])):
                assert_almost_equal(actual_results[step_location][location_coordinate], sequence_results[step_location][location_coordinate])

@patch.object(Greengraph, 'geolocate') # to account for method's dependancy on geolocate method. 
@patch.object(Map, 'count_green') # to account for method's dependancy on 'count_green' method in 'map' class.
@patch.object(requests, 'get') # to account for dependancy on the 'map' class where requests.get is used.
@patch.object(img, 'imread') # to account for method's dependancy on the 'map' class: count_green() -> green() -> Map() where 'imread' is used.
def test_green_between(mock_geolocate, mock_count_green, mock_requests_get, mock_imread):
    '''
    Test that green_between returns a list of green pixels for each step between two locations.
    '''
    
    with open(os.path.join(os.path.dirname(__file__), 'data', 'graph_data.yaml')) as dataset:
        green_between_data = yaml.load(dataset)['test_green_between']
    
    for data in green_between_data:
        first_location = data.pop('first_location')
        first_location_latlong = data.pop('first_location_latlong')
        second_location = data.pop('second_location')
        second_location_latlong = data.pop('second_location_latlong')
        steps = data.pop('steps')
        result = data.pop('result')
        
        mock_geolocate.side_effect = result
        mock_count_green.side_effect = [first_location_latlong, second_location_latlong]
        
        green_count = Greengraph(first_location, second_location).green_between(steps)
        assert_equal(result, green_count)

        
        
    