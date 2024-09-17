from setuptools import setup, find_packages

setup(
    name="Greengraph",
    version="0.1",
    description="Explore how green space varies between two locations.",
    url="https://github.com/AnoshZahir/Greengraph.git",
    licence="MIT",
    author="Anosh Zahir",
    author_email = "", # To be added in future.
    packages=find_packages(),  # Include all packages, including test files
    scripts=['scripts/graph'],
    install_requires=[
        'argparse',
        'geopy',
        'matplotlib',
        'requests',
        'numpy',
        'mock',
        'nose'  # Include nose for testing
    ],
    python_requires='>=3.5'
)
