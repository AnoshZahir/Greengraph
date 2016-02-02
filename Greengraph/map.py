import numpy as np
from StringIO import StringIO
from matplotlib import image as img
import requests

class Map(object):
    def __init__(self, lat, long, satellite = True, zoom = 10, size = (400, 400), sensor = False):
        """
        Construct a URL.
        Then assign to self.pixels the numpy array of the PNG image of the googlemaps location in the URL.
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
        Take the array to which 'self.pixels' points to.  Use the 'threshold' and return an array of True/False values depending on 
        whether each pixel is green or not. 
        """
	greener_than_red = self.pixels[:,:,1] > threshold*self.pixels[:,:,0]
	greener_than_blue = self.pixels[:,:,1] > threshold*self.pixels[:,:,2]
	green = np.logical_and(greener_than_red, greener_than_blue)
        return green # 400x400 array of true/false values. 
	
    def count_green(self, threshold = 1.1):
        """
        Take as argument a 'threshold' and return the number of green pixels in the image.
        """
        return np.sum(self.green(threshold))
	
    def show_green(self, threshold = 1.1):
        """
        
        """
        green = self.green(threshold) # return an array of true/false 
        out = green[:,:,np.newaxis]*np.array([0,1,0])[np.newaxis, np.newaxis, :]
        buffer = StringIO()
        result = img.imsave(buffer, out, format = 'png')
        return buffer.getvalue()
	