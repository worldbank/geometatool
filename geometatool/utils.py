# -*- coding: utf-8 -*-

import logging
import pandas as pd
from pyproj import Proj, transform
import dateutil.parser as dparser
from datetime import datetime
import re
import logging


#Set up logging
log = logging.getLogger(__name__)
  
# def EPSGfromWKT(wkt):
#     """ 
#     Function to get the EPSG code from the WKT (Well-Known-Text).
    
#     Arguments: 
#         wkt: The WKT.
#     """
#     try:
#         ident = Sridentify(prj=str(wkt))
#         EPSG = ident.get_epsg()
#     except:
#         log.error('Failed to get EPSG from WKT')
#         raise
    
#     return str(EPSG)


def BBOX_to_WGS84(BBOX, inputProjectionEPSG):
    """ 
    Function to transform Bounding Box coordinates to WGS84 for lat, long 
    representation in ISO19115-3 xml.
    
    Arguments: 
        BBOX (array): The BBOX to tranform.
        inputProjectionEPSG (string): The EPSG Code of the input BBOX.
    """
    try:
        #inProj = Proj(init='epsg:' + inputProjectionEPSG)
        inProj = Proj({'init': 'epsg:' + inputProjectionEPSG, 'no_defs': True}, preserve_flags=True)
        outProj = Proj(init='epsg:4326')
        #Careful with the order of the BBOX
        x = [BBOX[0], BBOX[2]]
        y = [BBOX[1], BBOX[3]] 
        x, y = transform(inProj,outProj,x, y)
        BBOX[0],BBOX[1], BBOX[2], BBOX[3] = x[0], y[0], x[1], y[1]
    except:
        log.error('Failed to convert Bounding Box to WGS84')
        raise

    return BBOX


def search_date(string):
    """ 
    Search for date information in a given string. 
      
    Arguments: 
        string (string): The string to be searched.
    """
    
    #Only consider strings that are longer then 4 characters
    if len(string)>4:
        #Search for format YYYY_MM_DD
        try:
            pattern = re.search(r'\d{4}_\d{2}_\d{2}',string)
            date = datetime.strptime(pattern.group(),'%Y_%m_%d').date()
            return date.strftime("%Y-%m-%d")
        except:
            pass
        #Search for format DD_MM_YYYY
        try:
            pattern = re.search(r'\d{2}_\d{2}_\d{4}',string)
            date = datetime.strptime(pattern.group(),'%d_%m_%Y').date()
            return date.strftime("%Y-%m-%d")
        except:
            pass
        #Search for formats with fuzzy logic using dateutil
        try:
            date = dparser.parse(string,fuzzy=True)
            return date.strftime("%Y-%m-%d")
        except:
            pass
        #Search for formats DDMMYYY
        try:
            pattern = re.search(r'\d{8}',string)
            date = datetime.strptime(pattern.group(),'%d%m%Y').date()
            return date.strftime("%Y-%m-%d")
        except:
            return 'undefined'
    else:
        log.debug('No date information available')
        return 'undefined'
        
    

def search_catchwords(string):
    """ 
    Splits String (at '_', '-' and '.' and searches for non-digit strings that
    are longer than 2 characters.
    
      
    Arguments: 
        string (string): The string to be searched.
    """

    #Exceptions that should not be considered Catchwords    
    exceptions = ['tif', 'aux', 'ref', 'etrs']
    
    #Create empty list
    Catchwords = []
    
    #Split list at underscores
    split_list_underscore = string.split('_') 
    for item in split_list_underscore:
        #Split items in list at points
        split_list_point = item.split('.')
        for item in split_list_point:
            #Split items in list at hyphen
            split_list = item.split('-')
            for item in split_list:
                #Make all items lowercase to enable removing duplicates with list(set())
                item = item.lower()
                if not item in exceptions:   
                    #Do not consider items with digits as Catchwords
                    if not item.isdigit():
                        if not len(item)<3:
                            Catchwords.append(item)

    return Catchwords 


ExtensionFormatData = [
    ["Vector",".SHP","Esri Shapefile"],
    ["Vector",".DBF","Esri Shapefile"],
    ["Vector",".SHX","Esri Shapefile"],
    ["Vector",".GEOJSON","Geographic JavaScript Object Notation"],
    ["Vector",".JSON","Geographic JavaScript Object Notation"],
    ["Vector",".GML","Geography Markup Language"],
    ["Vector",".KML","Google Keyhole Markup Language"],
    ["Vector",".KMZ","Google Keyhole Markup Language"],
    ["Vector",".GPX","GPS eXchange Format"],
    ["Vector",".VCT","IDRISI Vector"],
    ["Vector",".VDC","IDRISI Vector"],
    ["Vector",".TAB","MapInfo TAB"],
    ["Vector",".DAT","MapInfo TAB"],
    ["Vector",".ID","MapInfo TAB"],
    ["Vector",".MAP","MapInfo TAB"],
    ["Vector",".IND","MapInfo TAB"],
    ["Vector",".OSM","OpenStreetMap OSM XML"],
    ["Vector",".DLG","Digital Line Graph"],
    ["Raster",".IMG","ERDAS Imagine"],
    ["Raster",".ASC","American Standard Code for Information Interchange ASCII Grid"],
    ["Raster",".TIF","GeoTIFF"],
    ["Raster",".TIFF","GeoTIFF"],
    ["Raster",".OVR","GeoTIFF"],
    ["Raster",".RST","IDRISI Raster"],
    ["Raster",".RDC","IDRISI Raster"],
    ["Raster",".BIL","Envi RAW Raster"],
    ["Raster",".BIP","Envi RAW Raster"],
    ["Raster",".BSQ","Envi RAW Raster"],
    ["Raster",".PIX","PCI Geomatics Database File"],
    ["Compressed Raster",".ECW","ER Mapper Enhanced Compression Wavelet"],
    ["Compressed Raster",".JP2","Joint Photographic Experts Group JPEG2000"],
    ["Compressed Raster",".SID","LizardTech Multiresolution Seamless Image Database MrSID"],
    ["Compressed Raster",".SDW","LizardTech Multiresolution Seamless Image Database MrSID"],
    ["Geographic Database",".GDB","Esri File Geodatabase"],
    ["Geographic Database",".MDB","Esri Personal Geodatabase"],
    ["Geographic Database",".GPKG","OGC GeoPackage"],
    ["Geographic Database",".MBTILES","Mapbox MBTiles"],
    ["Geographic Database",".VMDS","GE Smallworld Version Managed Data Store"],
    ["Geographic Database",".SL3","SpatiaLite"],
    ["Geographic Database",".SQLITE","SpatiaLite"],
    ["LiDAR",".LAS","ASPRS LiDAR Data Exchange Format"],
    ["LiDAR",".LASD","ASPRS LiDAR Data Exchange Format"],
    ["LiDAR",".LAZ","ASPRS LiDAR Data Exchange Format"],
    ["LiDAR",".XYZ","Point Cloud XYZ"],
    ["CAD",".DWF","Autodesk Drawing"],
    ["CAD",".DWG","Autodesk Drawing"],
    ["CAD",".DXF","Autodesk Drawing"],
    ["CAD",".DGN","Bentley Microsystems DGN File Format"],
    ["Elevation",".DEM","USGS DEM, Canadian CDED"],
    ["Elevation",".DT0","Digital Terrain Elevation Data (DTED)"],
    ["Elevation",".DT1","Digital Terrain Elevation Data (DTED)"],
    ["Elevation",".DT2","Digital Terrain Elevation Data (DTED)"],
    ["Multitemporal",".NC","Network Common Data Form (NetCDF)"],
    ["Multitemporal",".HDF","Hierarchical Data Format"],
    ["Multitemporal",".GRIB","GRIdded Binary or General Regularly-distributed Information in Binary (GRIB)"],
    ["GIS Software Project",".MXD","Map Exchange Document"],
    ["GIS Software Project",".QGS","QGIS 2.X Project File"],
    ["GIS Software Project",".APRX","ArcGIS Pro Project File"],
    ["GIS Software Project",".QGZ","QGIS 3 Project File"],
    ["GIS Software Project",".MXT","Map Exchange Document Template"],
    ["GIS Software Project",".WOR","MapInfo Workspace"],
    ["GIS Software Project",".MWS","MapInfo Workspace"],
    ["GIS Software Project",".3DD","Esri ArcGlobe Document"],
    ["GIS Software Project",".SXD","Esri ArcScene Document"],
    ["GIS Software Project",".MAP","IDRISI Map Composition File"],
    ["Cartographic File",".LYR","Esri ArcGIS Layer File"],
    ["Cartographic File",".LYRX","Esri ArcGIS Layer File"],
    ["Cartographic File",".QLR","QGIS Layer Definition File"],
    ["Cartographic File",".STYL","Esri ArcGIS Style File"],
    ["Cartographic File",".STYLX","Esri ArcGIS Style File"],
    ["3D",".DAE","COLLADA"],
    ["3D",".SKP","Trimble Sketchup"],
    ["Interchange File",".E00","Esri ArcInfo Export (Interchange)"],
    ["Interchange File",".E01","Esri ArcInfo Export (Interchange)"],
    ["Interchange File",".MIF","MapInfo Interchange File"],
    ["Interchange File",".MID","MapInfo Interchange File"],
    ["Interchange File",".MPK","Map Package"],
    ["Indoor Mapping",".IMDF","Indoor Mapping Data Format"],
    ["Indoor Mapping",".AVF","Apple Venue Format"],
    ["Indoor Mapping",".RVT","Revit BIM"],
    ["Indoor Mapping",".NWD","Revit BIM"],
    ["Indoor Mapping",".DWG","Revit BIM"],
    ["Other",".TBX","Esri ArcGIS Toolbox"],
    ["Other",".SDE","ArcSDE Connection File"],
    ["Other",".PDF","Adobe Geospatial PDF"],
    ["Other",".ECD","Esri Classifier Definition"]
]

ExtensionFormatTable = pd.DataFrame(ExtensionFormatData, columns=['type','extension','format'])

def lookup_extension_format(extension):
    format_info = ExtensionFormatTable[ExtensionFormatTable['extension'] == extension]['format'].values
    return format_info[0] if len(format_info) > 0 else None

def lookup_extension_type(extension):
    type_info = ExtensionFormatTable[ExtensionFormatTable['extension'] == extension]['type'].values
    return type_info[0] if len(type_info) > 0 else None