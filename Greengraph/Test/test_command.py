"""
This module contains unit tests for the command-line functionality in the Greengraph project. 
It tests the argument parser, the green plotting functionality, and the overall process.
"""

from ..command import parser, green_plotter, process

from nose.tools import assert_equal, assert_true
from mock import patch

def test_command_line_arguments():
    """
    Test that the argument parser correctly assigns the arguments passed to it.

    This test ensures that the parser processes and assigns the correct values 
    to the first_location, second_location, steps, and output arguments.
    """
    arguments = parser.parse_args(['--from','London','--to','Cambridge','--steps', 4,'--out','my_file'])
    assert_equal( arguments.first_location, 'London')
    assert_equal( arguments.second_location, 'Cambridge')
    assert_equal( arguments.steps, 4)
    assert_equal( arguments.output, 'my_file')

@mock.patch('__main__'.Greengraph)
def test_green_plotter(mock_Greengraph)
    """
    Test the green_plotter function by mocking the Greengraph object, the plot function, and the savefig function.
    
    This test ensures that:
    - The Greengraph instance is created with the correct arguments.
    - The correct number of green pixels between two locations is plotted.
    - The plot is saved to the correct output file.
    """
    
@patch('command.parser.parse_args')
@patch('command.green_plotter')
def test_process(mock_parser, mock_green_plotter)
    """
    Test the overall process flow by ensuring that both the argument parser 
    and the green_plotter function are called during execution.
    """
    process()
    assert_true(mock_parser.called)
    assert_true(mock_green_plotter.called)