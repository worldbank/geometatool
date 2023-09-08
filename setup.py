import pathlib
from setuptools import setup, find_packages

BASE_DIR = pathlib.Path(__file__).parent

PACKAGE_NAME = 'GeoMetaTool'
VERSION = '0.0.1'
AUTHOR = 'Kamwoo Lee'
URL = 'https://github.com/klee016/GeoMetaTool'

LICENSE = 'GPLv3+'
DESCRIPTION = 'Geospatial Metadata Toolkit'
LONG_DESCRIPTION = (BASE_DIR / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = ['requests']

# Setting up
setup(
        name=PACKAGE_NAME,
        version=VERSION,
        author=AUTHOR,
        url=URL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type=LONG_DESC_TYPE,
        install_requires=INSTALL_REQUIRES,
        packages=find_packages(include=['GeoMetaTool'])
)
