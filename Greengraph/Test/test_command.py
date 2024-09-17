"""
This module contains unit tests for the command-line functionality in the Greengraph project. 
It tests the argument parser, the green plotting functionality, and the overall process.
"""
import unittest
from unittest.mock import patch
from ..command import parser, green_plotter, process

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

@patch('command.Greengraph')
@patch('matplotlib.pyplot.savefig')
@patch('matplotlib.pyplot.plot')
def test_green_plotter(mock_plot, mock_savefig, mock_Greengraph):
    """
    Test the green_plotter function by mocking the Greengraph object, the plot function, and the savefig function.
    
    This test ensures that:
    - The Greengraph instance is created with the correct arguments.
    - The correct number of green pixels between two locations is plotted.
    - The plot is saved to the correct output file.
    """
    mock_graph_instance = mock_Greengraph.return_value
    mock_graph_instance.green_between.return_value = [100, 200, 300, 400]  # Mock green pixel counts for test

    args = parser.parse_args(['--from', 'London', '--to', 'Cambridge', '--steps', '4', '--out', 'test_output'])
    
    green_plotter(args)
    
    # Check if Greengraph was initialized correctly
    mock_Greengraph.assert_called_with('London', 'Cambridge')

    # Check if green_between was called with the correct steps
    mock_graph_instance.green_between.assert_called_with(4)

    # Check if plot was called with the correct data
    mock_plot.assert_called_with([100, 200, 300, 400])

    # Check if the plot was saved to the correct output file
    mock_savefig.assert_called_with('test_output.png')
    
@patch('command.parser.parse_args')
@patch('command.green_plotter')
def test_process(mock_parser, mock_green_plotter):
    """
    Test the overall process flow by ensuring that both the argument parser 
    and the green_plotter function are called during execution.
    """
    process()
    assert_true(mock_parser.called)
    assert_true(mock_green_plotter.called)