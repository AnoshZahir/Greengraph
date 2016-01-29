from setuptools import setup, find_packages

setup(
    name = "Greengraph",
    version = "0.1",
    description = "Explore how green space varies between two locations.",
    url = "https://github.com/AnoshZahir/Greengraph.git",
    licence = "MIT",
    author = "Anosh Zahir",
    author_email = "anosh.zahir15@imperial.ac.uk",
    packages = find_packages(exclude = ['*test']),
    scripts = ['scripts/greengraph'],
    install_requires = ['argparse']
)

 