# -*- coding: utf-8 -*-

import logging
import os
import uuid
import time

from iso_metadata import *
from geo_profiles import vector_data
from geo_profiles import raster_data
from geo_profiles import geo_database
import utils


# set up logging
log = logging.getLogger(__name__)

def extract_metadata(input_file_path, default_values=[]):
    """ 
    Function to create an XML format metadata file. 
        
    Arguments: 
        output_file_path (string): The path of the output metadata file.   
    """

    input_file_path = input_file_path
    file_name_with_extension = os.path.basename(input_file_path)
    file_name = os.path.splitext(file_name_with_extension)[0]
    file_extension = os.path.splitext(file_name_with_extension)[1].upper()
    file_type = utils.lookup_extension_type(file_extension)
    file_format = utils.lookup_extension_format(file_extension)
    file_date = time.strftime('%Y-%m-%d', time.gmtime(os.path.getmtime(input_file_path)))

    if default_values:
        languageCode = default_values["languageCode"]
        characterSetCode = default_values["characterSetCode"]
        resourceScope = default_values["resourceScope"]
        organisationName = default_values["organisationName"]
        individualName = default_values["individualName"]
        roleCode = default_values["roleCode"]
        abstract = default_values["abstract"]
        keywords = default_values["keywords"]
        progressCode = default_values["progressCode"]
        timePeriod = default_values["timePeriod"]
        classificationCode = default_values["classificationCode"]
        useLimitations = default_values["useLimitations"]
    else:
        languageCode = "eng"
        characterSetCode = "UTF-8"
        resourceScope = "dataset"
        organisationName = "No name"
        individualName = "No name"
        roleCode = "author"
        abstract = "This file was automatically generated and has no abstract."
        keywords = []
        progressCode = ""
        timePeriod = ["", ""]
        classificationCode = ""
        useLimitations = ""
 
    iso_metadata = ISO_Metadata()

    ###############
    # Vector data #
    ###############
    if file_type == 'Vector':
        profiles = vector_data.read_profiles(input_file_path)

        # set vectorSpatialRepresentation
        vectorSpatialRepresentation = {}
        vectorSpatialRepresentation['topologyLevelCode'] = "geometryOnly"
        geometricObjectsList = []
        for geom_type, count in profiles['geometry_types_count'].items():
            if geom_type == 'Point':
                objectType = 'point'
            elif geom_type == 'LineString':
                objectType = 'curve'
            elif geom_type == 'Polygon':
                objectType = 'surface'
            else:
                objectType = 'complex'
            geometricObject = {}
            geometricObject['objectType'] = objectType
            geometricObject['count'] = count
            geometricObjectsList.append(geometricObject)
        vectorSpatialRepresentation['geometricObjectsList'] = geometricObjectsList
        
        # set featureTypeList
        featureTypeList = []
        characteristicsList = []
        for field_summary in profiles['field_summary_list']:
            characteristics = {}
            characteristics['memberName'] = field_summary['field_name']
            characteristics['valueType'] = field_summary['value_type']
            characteristics['listedValueList'] = field_summary['10_unique_values']
            characteristicsList.append(characteristics)
        featureType = {}
        featureType['typeName'] = profiles['layerName']
        featureType['definition'] = profiles['layerName']
        featureType['carrierOfCharacteristicsList'] = characteristicsList
        featureTypeList.append(featureType)

        # add elements
        iso_metadata.metadataIdentifier(str(uuid.uuid1()))   
        if languageCode and characterSetCode:
            iso_metadata.defaultLocale(languageCode, characterSetCode)
        if resourceScope:
            iso_metadata.metadataScope(resourceScope)
        iso_metadata.contact(organisationName, individualName, roleCode)
        iso_metadata.dateInfo(file_date, 'creation')
        if vectorSpatialRepresentation:
            iso_metadata.spatialRepresentationInfo(vectorSpatialRepresentation, None)
        if profiles['EPSG']:
            iso_metadata.referenceSystemInfo(profiles['EPSG'], profiles['referenceSystemTypeCode'])
        iso_metadata.identificationInfo(file_name, abstract, progressCode, None, profiles['BBOX'], timePeriod, file_format, keywords, classificationCode, useLimitations)
        if featureTypeList:
            iso_metadata.contentInfo(profiles['layerName'], [profiles['layerName']], "v", file_date, languageCode, organisationName, individualName, roleCode, featureTypeList)
        iso_metadata.distributionInfo('Offline File.', file_name_with_extension)
        


    ###############
    # Raster data #
    ###############
    elif file_type == 'Raster':
        profiles = raster_data.read_profiles(input_file_path)
    

    ################
    # Geo database #
    ################
    elif file_type == 'Geographic Database':
        profiles = geo_database.read_profiles(input_file_path)
    
    else:
        raise Exception(f"This package does not support {file_type}.")
    
    return iso_metadata
