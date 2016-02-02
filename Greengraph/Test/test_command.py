from ..command import parser, green_plotter, process
from ..graph import Greengraph
from ..map import Map

from nose.tools import assert_equal, assert_true
from mock import mock_open, patch

def test_command_line_arguments():
    '''
    Test that argument parser correctly assigns the arguments passed to it.
    '''
    arguments = parser.parse_args(['--from','London','--to','Cambridge','--steps', 4,'--out','my_file'])
    assert_equal( arguments.first_location, 'London')
    assert_equal( arguments.second_location, 'Cambridge')
    assert_equal( arguments.steps, 4)
    assert_equal( arguments.output, 'my_file')


'''
patch replaces MyClass in a way that allows you to control the usage of the class in functions that you call. 
Once you patch a class, references to the class are completely replaced by the mock instance.

mock.patch is usually used when you are testing something that creates a new instance of a class inside of the test.  
mock.Mock instances are clearer and are preferred. If your self.sut.something method created an instance of MyClass 
instead of receiving an instance as a parameter, then mock.patch would be appropriate here.
'''

@mock.patch('__main__'.Greengraph) #based on the above notes, use @mock.patch as in green_plotter method, 'this_graph' is an instance of Greengraph.
def test_green_plotter(mock_Greengraph):
    
@patch('command.parser.parse_args')
@patch('command.green_plotter')
def test_process(mock_parser, mock_green_plotter)
    process()
    assert_true(mock_parser.called)
    assert_true(mock_green_plotter.called)
