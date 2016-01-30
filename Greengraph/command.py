from matplotlib import pyplot as plt
from graph import Greengraph
from argparse import ArgumentParser

def process():
    parser = ArgumentParser(description = "Explore how green space varies between two locations.")
	
    parser.add_argument('first_location', help = 'enter name of first location', type = str)
    parser.add_argument('second_location',help = 'enter name of second location', type = str)
    parser.add_argument('steps', help = 'enter the number of steps between the two locations', type = int)
    parser.add_argument('out', help= 'enter name of output file: format .png')
    
    arguments = parser.parse_args()
    
    
if __name__ == "__main__":
    process()