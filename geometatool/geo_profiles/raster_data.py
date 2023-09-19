import os
import rasterio
import logging
import numpy as np
# import importlib
# utils = importlib.import_module("utils", package="..utils")

#Set up logging
log = logging.getLogger(__name__)

def read_profiles(file_path):
    """ 
    read profiles of raster data 
        
    Arguments: 
        file_path (string): The path of the file to be opened.
        extension (string): The extension of the file   
    """
    profiles = {}
    profiles['EPSG'] = None
    profiles['BBOX'] = None
    profiles['referenceSystemTypeCode'] = None
    profiles['layerName'] = None
    profiles['numberOfDimensions'] = 2
    profiles['width'] = None
    profiles['height'] = None
    profiles['transform'] = None


    file_name_with_extension = os.path.basename(file_path)
    file_name, file_extension = os.path.splitext(file_name_with_extension)

    if file_extension.upper() == '.TIF' or file_extension.upper() == '.TIFF' :
        log.debug('Opening TIF file')
        try:
            ras_content = rasterio.open(file_path)
        except:
            log.error('Failed to open TIFF file')
            raise

        profiles['layerName'] = file_name

        # Set referenceSystemTypeCode
        profiles['referenceSystemTypeCode'] = 'geodeticGeographic2D'

        # Get EPSG
        profiles['EPSG'] = str(ras_content.crs.to_epsg())

        # Get bounding box
        profiles['BBOX'] = [0,0,0,0]
        profiles['BBOX'][0], profiles['BBOX'][2], profiles['BBOX'][1], profiles['BBOX'][3] = ras_content.bounds 
        if profiles['EPSG'] != '4326':
            profiles['BBOX'] = utils.BBOXtoWGS84(profiles['BBOX'], profiles['EPSG'])
        profiles['BBOX'][0] = str(profiles['BBOX'][0])
        profiles['BBOX'][1] = str(profiles['BBOX'][1])
        profiles['BBOX'][2] = str(profiles['BBOX'][2])
        profiles['BBOX'][3] = str(profiles['BBOX'][3])

        # Get width
        profiles['width'] = ras_content.width

        # Get height
        profiles['height'] = ras_content.height

        # Get unit
        if ras_content.crs.is_geographic:
            profiles['unit'] = "decimalDegrees"
        else:
            profiles['unit'] = ras_content.crs.linear_units

        # Get numberOfBands
        profiles['numberOfBands'] = ras_content.count
        
        # Get min/max values
        profiles['maxValues'] = []
        profiles['minValues'] = []
        for band_idx in range(ras_content.count):
            profiles['maxValues'].append(np.nanmax(ras_content.read(band_idx+1)))
            profiles['minValues'].append(np.nanmin(ras_content.read(band_idx+1)))
        
        # Get noData value
        profiles['noDataValue'] = str(ras_content.nodata)

        # Get affine transform
        profiles['transform'] = ras_content.transform

    return profiles


                