import numpy as np
from StringIO import StringIO
from matplotlib import image as img
import requests

class Map(object):
    def __init__(self, lat, long, satellite = True, zoom = 10, size = (400, 400), sensor = False):
        """
        Method to construct a URL.
        The first part of the URL is in the 'base' variable in the method's body.
        The rest of the URL is constructed from key/value pairs given by arguments
        latitude, longitude, satellite, zoom, size and sensor.
        
        The Response object 'self.image' points to the data returned by 
        response.get().content. The data is of the PNG image of the google maps location.
        Finally, 'self.image points to the numpy array of the PNG image.
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
	
    def green(self, threshold):
        """
        Given an argument threshold, the function takes the array 'self.pixels' 
        points to and returns an array of True/False values depending of 
        whether each pixel is green or not. 
        """
	greener_than_red = self.pixels[:,:,1] > threshold*self.pixels[:,:,0]
	greener_than_blue = self.pixels[:,:,1] > threshold*self.pixels[:,:,2]
	green = np.logical_and(greener_than_red, greener_than_blue)
        return green
	
    def count_green(self, threshold = 1.1):
        """
        Takes as argument a 'threshold' and returns the number of green pixels in the image.
        """
        return np.sum(self.green(threshold))
	
    def show_green(self, threshold = 1.1):
        green = self.green(threshold)
        out = green[:,:,np.newaxis]*np.array([0,1,0])[np.newaxis, np.newaxis, :]
        buffer = StringIO()
        result = img.imsave(buffer, out, format = 'png')
        return buffer.getvalue()
	