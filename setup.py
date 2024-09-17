from setuptools import setup, find_packages

setup(
    name="Greengraph",
    version="0.1",
    description="A Python package to explore how green space varies between two locations using satellite imagery.",
    url="https://github.com/AnoshZahir/Greengraph.git",
    license="MIT",
    author="Anosh Zahir",
    author_email = "", # To be added in future.
    packages=find_packages(),  # Automatically find all packages
    scripts=['scripts/graph'], # Include the script for command-line usage
    install_requires=[
        'argparse',
        'geopy',
        'matplotlib',
        'requests',
        'numpy',
        'mock'
    ],
    python_requires='>=3.5' # Specify the required Python version
)
