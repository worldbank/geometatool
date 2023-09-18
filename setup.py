import pathlib
from setuptools import setup, find_packages

BASE_DIR = pathlib.Path(__file__).parent

PACKAGE_NAME = 'geometatool'
VERSION = '0.0.19'
AUTHOR = 'Kamwoo Lee'
URL = 'https://github.com/worldbank/geometatool'

LICENSE = 'GPLv3+'
DESCRIPTION = 'Geospatial Metadata Toolkit'
LONG_DESCRIPTION = (BASE_DIR / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = ['requests', 'xmltodict', 'pandas', 'geopandas', 'rasterio', 'numpy', 'jsonschema', 'lxml', 'pyproj']

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
        packages=find_packages(include=['geometatool', 'geometatool.geo_profiles']),
        include_package_data=True,
        package_data={'': ['geometatool']},
)
