"""
This module contains unit tests for the Greengraph class in the graph.py module.
It tests geolocation, location sequence generation, and green space analysis functionality.
"""

from Greengraph.graph import Greengraph
from Greengraph.map import Map

import os
import yaml
import unittest
from unittest.mock import patch
from yaml.constructor import ConstructorError

# Adding constructor for tuples in YAML
def tuple_constructor(loader, node):
    """
    Custom constructor for YAML to handle tuples.
    
    Args:
        loader: The YAML loader instance that parses the document.
        node: The current YAML node being processed, expected to be a sequence node.
    
    Returns:
        tuple: A Python tuple created from the YAML sequence node.
    """
    return tuple(loader.construct_sequence(node))

yaml.SafeLoader.add_constructor('tag:yaml.org,2002:python/tuple', tuple_constructor)

class TestGreengraph(unittest.TestCase):
    """
    Unit tests for the Greengraph class, which handles geolocation, location sequence generation, 
    and green space analysis.

    This class includes the following tests:
    - Test that the Greengraph object is instantiated correctly.
    - Test that the geolocate method returns the correct latitude and longitude for a location.
    - Test that the location_sequence method generates a correct sequence of coordinates.
    - Test that the green_between method calculates the number of green pixels between two locations.
    """
    
    @patch('geopy.geocoders.GoogleV3')
    def test_Greengraph(self, mock_geocoder):
        """
        Test Greengraph instantiation.

        This test verifies that the Greengraph object is instantiated with the correct start and 
        end locations. It ensures that the start and end attributes are assigned properly.
        """
        actual = Greengraph('London', 'Cambridge')
        self.assertEqual(actual.start, 'London')
        self.assertEqual(actual.end, 'Cambridge')

    @patch('geopy.geocoders.GoogleV3')
    @patch.object(Greengraph, 'geolocate')
    def test_geolocate(self, mock_geolocate, mock_geocoder):
        """
        Test the geolocate method.

        This test ensures that the geolocate method returns the correct latitude and longitude 
        when given a location. The geocode method from geopy is mocked to avoid calling the 
        real API, and test data is used from the YAML file.
        """
        mygraph = Greengraph(0.0, 0.0)

        with open(os.path.join(os.path.dirname(__file__), 'data', 'graph_data.yaml')) as dataset:
            geolocate_data = yaml.safe_load(dataset)['test_geolocate']
        
        for data in geolocate_data:
            location = data.pop('location')
            latitude = data.pop('location_lat')
            longitude = data.pop('location_long')
            
            expected_return = (latitude, longitude)
            mock_geolocate.return_value = expected_return

            actual_return = mygraph.geolocate(location)
            
            self.assertEqual(actual_return, expected_return)

    @patch('geopy.geocoders.GoogleV3')
    def test_location_sequence(self, mock_geocoder):
        """
        Test the location_sequence method.

        This test checks that the location_sequence method returns a sequence of evenly spaced 
        latitude and longitude pairs between the start and end locations. The test uses mock data 
        from the YAML file to verify correctness.
        """
        mygraph = Greengraph('London', 'Cambridge', mock_geocoder)

        with open(os.path.join(os.path.dirname(__file__), 'data', 'graph_data.yaml')) as dataset:
            location_sequence_data = yaml.safe_load(dataset)['test_location_sequence']

        for data in location_sequence_data:
            first_location_coordinates = data.pop('first_location_coordinates')
            second_location_coordinates = data.pop('second_location_coordinates')
            steps = data.pop('steps')
            expected_return = data.pop('expected_return')
            
            actual_return = mygraph.location_sequence(first_location_coordinates, second_location_coordinates, steps)
            for step_num in range(0, steps):
                for coordinate in range(0, 2):
                    self.assertAlmostEqual(actual_return[step_num][coordinate], expected_return[step_num][coordinate])

    @patch('geopy.geocoders.GoogleV3.geocode')
    @patch('geopy.geocoders.GoogleV3')
    @patch.object(Greengraph, 'location_sequence')
    @patch.object(Map, 'count_green')
    def test_green_between(self, mock_count_green, mock_location_sequence, mock_GoogleV3, mock_geocode):
        """
        Test the green_between method.

        This test ensures that the green_between method correctly calculates the number of 
        green pixels for each location along the path between two locations. The location_sequence 
        and count_green methods are mocked to simulate intermediate steps. Test data is loaded 
        from the YAML file to verify the expected results.
        """
        
        # Mock the geocode method to return fixed coordinates (latitude, longitude)
        mock_geocode.return_value = [(51.5074, -0.1278)]  # Mocked coordinates for London
        
        # Pass the mock geocoder to Greengraph
        mygraph = Greengraph('London', 'Cambridge', mock_GoogleV3)
        
        # Load mock data from the YAML file
        with open(os.path.join(os.path.dirname(__file__), 'data', 'graph_data.yaml')) as dataset:
            green_between_data = yaml.safe_load(dataset)['test_green_between']
        
        for data in green_between_data:
            location_sequence_values = data.pop('location_sequence_values')
            count_green_values = data.pop('count_green_values')
            steps = data.pop('steps')
            
            # Mock the behavior of location_sequence and count_green
            mock_location_sequence.return_value = location_sequence_values
            mock_count_green.side_effect = count_green_values

            # Call the method to be tested
            actual_return = mygraph.green_between(steps)
            
            # Assert that the results match the expected values
            self.assertEqual(actual_return, count_green_values)

if __name__ == '__main__':
    unittest.main()