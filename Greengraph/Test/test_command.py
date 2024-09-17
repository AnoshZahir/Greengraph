"""
This module contains unit tests for the command-line functionality in the Greengraph project. 
It tests the argument parser, the green plotting functionality, and the overall process.
"""

from ..command import parser, green_plotter, process

from nose.tools import assert_equal, assert_true

from mock import patch

def test_command_line_arguments():
    '''
    Test that argument parser correctly assigns the arguments passed to it.
    '''
    arguments = parser.parse_args(['--from','London','--to','Cambridge','--steps', 4,'--out','my_file'])
    assert_equal( arguments.first_location, 'London')
    assert_equal( arguments.second_location, 'Cambridge')
    assert_equal( arguments.steps, 4)
    assert_equal( arguments.output, 'my_file')

@mock.patch('__main__'.Greengraph)
def test_green_plotter(mock_Greengraph)
    #update with code.
    
@patch('command.parser.parse_args')
@patch('command.green_plotter')
def test_process(mock_parser, mock_green_plotter)
    process()
    assert_true(mock_parser.called)
    assert_true(mock_green_plotter.called)