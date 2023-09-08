# -*- coding: utf-8 -*-

import os
from lxml import etree
import json
import jsonschema
                                                  

def validate_xml_ISO19115_3(instance_file):  
    """ 
    Function to check a XML file for syntax errors and validate it against the ISO19115-3 schemas.
    The schemas are stored in the iso folder.
    
    Arguments: 
        instance_file: The path of the XML file to be validated.
    """
                                  
    # open schema file   

    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))                                                       
    # schema_file = os.path.join(BASE_DIR, "iso_standards/19115/-3/mdt/2.0/mdt.xsd")                                                                                                                                     
    # with open(schema_file) as f:                                   
    #     xsd = etree.parse(f)
    #     schema = etree.XMLSchema(xsd)


    BASE_DIR = os.path.dirname(os.path.abspath(__file__))                                                       
    schema_file = os.path.join(BASE_DIR, "iso_standards/19115/-3/mdt/2.0/mdt.xsd")                                                                                                                                     
    with open(schema_file) as f:                                   
        xsd = etree.parse(f)
        gfc_import = etree.Element('{http://www.w3.org/2001/XMLSchema}import',
                                    namespace="http://standards.iso.org/iso/19110/gfc/1.1",
                                    schemaLocation="../../../../19110/gfc/1.1/gfc.xsd")
        xsd.getroot().append(gfc_import)
        schema = etree.XMLSchema(xsd)
                                                                                                        
    # open instance file
    file_extension = os.path.splitext(instance_file)[1].upper()
    if file_extension != '.XML':
        raise Exception("The instance file is not XML.")

    # validate instance against schema
    with open(instance_file) as f:
        try:
            doc = etree.parse(f)
            print('The XML is well formed.')
        except etree.XMLSyntaxError as err:
            print(err)
                                                                                                      
        try:
            schema.assertValid(doc)
            print('The instance is valid aginst the ISO 19115-3 and ISO 19110 schemas.')
        except etree.DocumentInvalid as err:
            print(err)
    

def validate_json(instance_file, schema_file):
    """ 
    Function to check a JSON file for syntax errors and validate it against the provided schema.
    
    Arguments: 
        instance_file: The path of instance JSON file
        schema_file: The path of schema JSON file
    """

    # open schema file
    file_extension = os.path.splitext(schema_file)[1].upper()
    if file_extension != '.JSON':
        raise Exception("The schema file is not JSON.")
    with open(schema_file) as f:
        schema = json.load(f)
                                                                                                        
    # open instance file
    file_extension = os.path.splitext(instance_file)[1].upper()
    if file_extension != '.JSON':
        raise Exception("The instance file is not JSON.")
    with open(instance_file) as f:
        instance = json.load(f)

    # validate instance against schema
    try:
        jsonschema.validate(instance=instance, schema=schema)
        print('The instance is valid aginst the provided schema.')
    except jsonschema.exceptions.SchemaError as err:
        print(err)
    except jsonschema.exceptions.ValidationError as err:
        print(err)


