""""
This module contains the Greengraph class, which includes methods for geolocation,
generating location sequences, and analyzing green space between two specified locations.
"""

import numpy as np
import geopy
from map import Map

class Greengraph(object):
	def __init__(self, start, end):
	    """
	    Instantiate graph object with arguments 'start' and 'end'
	    """
	    self.start = start
	    self.end = end
	    self.geocoder = geopy.geocoders.GoogleV3(domain = "maps.google.co.uk")
	
	def geolocate(self, place):
	    """
	    Take one argument 'place' and return a tuple for that location's latitude and longitude.
	    """
	    return self.geocoder.geocode(place, exactly_one = False)[0][1]
		
	def location_sequence(self, start, end, steps):
	    """
	    Return according to 'steps' an evenly spaced set of places between the 'start' and 'end' locations. 
	    """
	    lats = np.linspace(start[0], end[0], steps)
	    longs = np.linspace(start[1], end[1], steps)
	    return np.vstack([lats, longs]).transpose()
	
	def green_between(self, steps):
	    """
	    Return the number of green pixels for each point between two locations.
	    """
	    return [Map(*location).count_green()
		for location in self.location_sequence(
		  self.geolocate(self.start),
		  self.geolocate(self.end),
		  steps)]