import os
import geopandas as gpd
import logging
import utils

#Set up logging
log = logging.getLogger(__name__)

def read_profiles(file_path):
    """ 
    read profiles of vector data 
        
    Arguments: 
        file_path (string): The path of the file to be opened.
        extension (string): The extension of the file
    """
    profiles = {}
    profiles['EPSG'] = None
    profiles['BBOX'] = None
    profiles['referenceSystemTypeCode'] = None
    profiles['geometry_types_count'] = None
    profiles['layerName'] = None
    profiles['field_summary_list'] = []

    file_name_with_extension = os.path.basename(file_path)
    file_name, file_extension = os.path.splitext(file_name_with_extension)

    if file_extension.upper() == '.SHP':
        log.debug('Opening Shapefile')
        try:
            gdf_content = gpd.read_file(file_path)
        except:
            log.error('Failed to open Shapefile')
            raise

        profiles['layerName'] = file_name

        # Set referenceSystemTypeCode
        profiles['referenceSystemTypeCode'] = 'geodeticGeographic2D'

        # Get EPSG
        profiles['EPSG'] = str(gdf_content.crs.to_epsg())

        # Get bounding box
        profiles['BBOX'] = [0,0,0,0]
        profiles['BBOX'][0], profiles['BBOX'][2], profiles['BBOX'][1], profiles['BBOX'][3] = gdf_content.total_bounds 
        if profiles['EPSG'] != '4326':
            profiles['BBOX'] = utils.BBOXtoWGS84(profiles['BBOX'], profiles['EPSG'])
        profiles['BBOX'][0] = str(profiles['BBOX'][0])
        profiles['BBOX'][1] = str(profiles['BBOX'][1])
        profiles['BBOX'][2] = str(profiles['BBOX'][2])
        profiles['BBOX'][3] = str(profiles['BBOX'][3])

        # Get the number of each geometry type
        profiles['geometry_types_count'] = gdf_content['geometry'].geom_type.value_counts()

        profiles['layer_name'] = file_name
        # Get summary info on each field            
        for column_name in gdf_content.columns:
            if column_name == 'geometry':
                continue
            field_summary = {}
            field_summary['field_name'] = column_name
            field_summary['value_type'] = str(gdf_content[column_name].dtype)
            field_summary['num_unique_values'] = len(gdf_content[column_name].unique())
            field_summary['10_unique_values'] = gdf_content[column_name].unique()[:10]
            profiles['field_summary_list'].append(field_summary)

        return profiles


                