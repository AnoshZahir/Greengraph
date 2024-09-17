"""
This module handles the command-line interface (CLI) for the Greengraph project.
It allows users to input two locations and the number of steps between them, 
and generates a plot representing the green space between the two points.
The output is saved as a .png image.
"""

from matplotlib import pyplot as plt
from graph import Greengraph
from argparse import ArgumentParser

# Argument parser for the command-line interface
parser = ArgumentParser(description = "Explore how green space varies between two locations.")

parser.add_argument('-f', '--from', default='London', dest='first_location', type=str, required=False, 
                    help='Enter name of the first location as a string. Default set to "London".')
parser.add_argument('-t', '--to', default='Cambridge', dest='second_location', type=str, required=False, 
                    help='Enter name of the second location as a string. Default set to "Cambridge".')
parser.add_argument('-s', '--steps', dest='steps', type=int, default=10, 
                    help='Enter the number of steps between the two locations. Optional, default set to 10 steps.')
parser.add_argument('-o', '--out', dest='output', default='output', 
                    help='Enter the name of the output file. The file will be saved as a .png.')
    
def green_plotter(arguments):
    """
    Generates a plot showing the green space between two locations.
    
    Args:
        arguments: Parsed command-line arguments including:
            - first_location: The starting location.
            - second_location: The ending location.
            - steps: Number of steps between the two locations.
            - output: The output file name for the .png plot.
    """
    this_graph = Greengraph(arguments.first_location, arguments.second_location)# create an instance of the Greengraph class object.
    green_count = this_graph.green_between(arguments.steps)
    
    # Plot green pixel counts between locations
    plt.plot(green_count)
    plt.title(f'Number of green pixels between {arguments.first_location} and {arguments.second_location}')
    plt.xlabel('Steps')
    plt.ylabel('Green pixels')
    
    # Save plot to a .png file
    plt.savefig(f'{arguments.output}.png')
    plt.show()

def process() -> None:
    """
    Parses the command-line arguments and invokes the green_plotter function.
    """
    arguments = parser.parse_args()
    green_plotter(arguments)
    
if __name__ == "__main__":
    process()
