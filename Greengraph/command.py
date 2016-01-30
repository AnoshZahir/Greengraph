from matplotlib import pyplot as plt
from graph import Greengraph
from argparse import ArgumentParser

parser = ArgumentParser(description = "Explore how green space varies between two locations.")

parser.add_argument('first_location', help = 'enter name of first location', type = str)
parser.add_argument('second_location',help = 'enter name of second location', type = str)
parser.add_argument('steps', help = 'enter the number of steps between the two locations', type = int)
parser.add_argument('out', help= 'enter name of output file: format .png')
    
def green_plotter(arguments):
    this_graph = Greengraph(arguments.first_location, arguments.second_location)# create an instance of the Greengraph class object.
    green_count = this_graph.green_between(arguments.steps)
    plt.plot(green_count)
    
    plt.title('Number of green pixels in locations between ' + arguments.first_place + ' and ' + arguments.second_place) 
    plt.xlabel('Steps')
    plt.ylabel('Geen pixels')
    
    plt.savefig(arguments.out)
    plt.show()

def process():
    arguments = parser.parse_args()
    green_plotter(arguments)
    
if __name__ == "__main__":
    process()