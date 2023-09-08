import os
import geopandas as gpd
import logging
import utils

#Set up logging
log = logging.getLogger(__name__)

def read_geo_database(file_path, extension):
    """ 
    read profiles of geospatial database
        
    Arguments: 
        file_path (string): The path of the file to be opened.
        extension (string): The extension of the file
    """
    profiles = {}

    return profiles