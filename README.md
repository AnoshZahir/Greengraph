Greengraph package
==================

This package is about how urbanised the world is, based on satellite imagery, along a line betwen two cities.  We expect the satellite image to be greener in the countryside.

The package contains two classes - Greengraph and Map.  The outcome is a png image of a graph which plots the number of green pixels at regular intervals between two locations.


### How to install:

The package has been setup so that it can be pip installed:
* Download the package
* Go to the package's root directory using the command line
* Depeding on your machine:
    * Windows: python setup.py install
    * Mac/other: sudo python setup.py install
* Package can also be installed from: https://github.com/AnoshZahir/Greengraph.git

### How to use via command line:

--from (or -f) and --to (-t) for the two locations betweeen which the green space should be evaluated.

--steps(or -s) for the number of intervals between the two locations.

--out or(-o) to give a filename for the output graph.  'You must only provide the file_name as '.png' will be added to the file_name by default.  The 'file_name.png' will be saved in the same directory from where the call was made.

Example command line: Greengraph -f 'london' -t 'cambridge' -s 4 -o file_name
