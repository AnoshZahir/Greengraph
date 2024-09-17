# Greengraph Package

This package provides tools to evaluate how urbanized the world is based on satellite imagery along a line between two cities. The satellite images will show greener areas in the countryside compared to urban spaces.

The package contains two classes: `Greengraph` and `Map`. The final output is a `.png` image of a graph that plots the number of green pixels at regular intervals between two locations.

## How to Install

The package is set up to be installed via `pip`. To install the package:

1. Download the package.
2. Go to the package's root directory using the command line.
3. Run the following commands depending on your machine:
    - **Windows:** `python setup.py install`
    - **Mac/Linux:** `sudo python setup.py install`

Alternatively, you can install the package from the GitHub repository:

```bash
pip install git+https://github.com/AnoshZahir/Greengraph.git
```

## How to use via command line:

You can use the following command-line arguments to evaluate green space between two locations:

- --from (or -f): The starting location.
- --to (or -t): The destination location.
- --steps (or -s): The number of intervals between the two locations.
- --out (or -o): The filename for the output graph (Do not add the .png extension; it will be added automatically).

Example command line:
```bash 
$ Greengraph -f 'london' -t 'cambridge' -s 4 -o file_name
```
This command will generate a graph showing green space between London and Cambridge, saving the result as file_name.png.

## Project History
While I initially developed this project in 2015 as part of UCL’s "MPHYG001 Research Software Engineering with Python" course, I revisited the project in September 2024 to bring it up to date with the latest version of Python, modern libraries, and current development practices. This modernization ensures the code is compatible with contemporary tools and runs efficiently in today's software environments.

## Lessons Learned
Throughout this project, I gained valuable experience in the following areas:

- **Version control with Git**: Used Git and GitHub to manage and track changes, ensuring proper versioning throughout development. I also applied branch management techniques to manage features and bug fixes in an organized manner.
- **Creating and distributing Python packages**: Learned how to structure and package Python code for easy installation and distribution via pip. This included understanding packaging requirements, creating setup scripts, and ensuring the package is ready for others to install and use efficiently.
- **Test-driven development (TDD)**: Refined my ability to write and update unit tests to ensure the robustness of the codebase.
- **Mocking and patching**: Implemented mocking techniques to simulate external dependencies in unit tests, helping isolate specific behaviors for more effective testing.
- **Working with geospatial data**: Learned how to work with geospatial libraries and APIs such as Google Maps, and how to extract and process satellite images.
- **Image processing**: Gained experience in manipulating image data, including working with pixel matrices and evaluating pixel-based criteria.
- **Updating legacy code**: Modernized code written in 2015, ensuring compatibility with new versions of Python and libraries, such as NumPy, Matplotlib, and Requests.

These skills are crucial for maintaining and improving software in a professional environment, and they have significantly enhanced my expertise in both software engineering and data analysis.

## Expanded Use Cases
This package can be applied to a variety of fields and research areas, including:

- **Environmental Research**: By analyzing satellite images, researchers can assess deforestation, urban expansion, and the impact of human activity on green spaces. This tool provides a quantitative method to evaluate changes in vegetation across regions.
- **Urban Planning and Development**: Urban planners can use this tool to compare the green spaces between cities and rural areas, helping to make data-driven decisions about sustainable urban development and environmental impact assessments.
- **Education and Training**: The package serves as a valuable educational tool for teaching satellite image processing, geospatial analysis, and Python programming. It can also be used in classroom settings to demonstrate practical applications of software engineering principles.

## Citation
This package is based on the course "MPHYG001 Research Software Engineering with Python" from UCL's Autumn 2015 term. If you wish to refer to this course, please cite the following URL:

[Citation for UCL Python Course](http://development.rc.ucl.ac.uk/training/engineering)

**Note:** The site address may change over time. If the above link is out of date or broken, please search online for the course title or check UCL's current course offerings for the latest version.


## License
This project is licensed under the [MIT License](https://opensource.org/license/MIT).