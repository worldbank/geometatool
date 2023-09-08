import os
import csv
import json
import xmltodict
import pandas as pd


def flatten_dict(indict, path=''):
    """ 
    Recursive function to flatten a dictionary object and return it as a generator

    Arguments: 
        indict: partial or full dict
        path: partial or full path
    """
    if isinstance(indict, dict):
        for key, value in indict.items():
            if isinstance(value, dict):
                new_path = path + "/" + key if path else key
                for d in flatten_dict(value, new_path):
                    yield d
            elif isinstance(value, list) or isinstance(value, tuple):
                for v in value:
                    new_path = path + "/" + key if path else key
                    for d in flatten_dict(v, new_path):
                        yield d
            else:
                new_path = path + "/" + key if path else key
                yield {"path": new_path, "value": value}
    else:
        yield {"path": path, "value": indict}


def lookup_converted_paths(original_path, conversion_table):
    """ 
    Function to lookup converted paths based on a conversion table

    Arguments: 
        original_path: flattened original path
        conversion_table: mapping table between original path (first column) and target path (second column)
    """
    paths = conversion_table[conversion_table.iloc[:, 0] == original_path]
    if not paths.empty:
        return list(paths.iloc[:, 1])
    else:
        return None
    

def get_partial_schema(schema, partial_path):
    """ 
    Function to return a partial schema for the given partial path

    Arguments: 
        schema: schema from which to extract a partial schema
        partial_path: list of elements that make up a partial path
    """
    partial_schema = schema
    for element in partial_path:
        element_type = partial_schema['type']
        if element_type == 'object':
            partial_schema = partial_schema['properties'][element]
        elif element_type == 'array':
            partial_schema = partial_schema['items']['properties'][element]
        else:
            partial_schema = None
    return partial_schema


def read_metadata_items(input_file_path, output_file_path=None):
    extension = os.path.splitext(input_file_path)[1].upper()
    if extension == '.JSON':
        with open(input_file_path) as f:
            metadata_item_generator = flatten_dict(json.load(f))
    elif extension == '.XML':
        with open(input_file_path) as f:
            metadata_item_generator = flatten_dict(xmltodict.parse(f.read()))
    else:
        raise Exception("Input file must be in JSON or XML format.")

    if output_file_path:
        with open(output_file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows([[item['path'], item['value']] for item in metadata_item_generator])

    return list(metadata_item_generator)


def convert_metadata(input_file_path, conversion_table_file_path, target_schema_file_path):
    """ 
    Function to convert metadata from one schema to another

    Arguments: 
        input_file_path (str): Original metadata.
        conversion_table_file_path (str): The file containing conversion mapping between original metadata items and target metadata items.
        target_schema_file_path (str): The schema to which the metadata will be converted.
    """
    
    # read original metadata
    original_metadata_items = read_metadata_items(input_file_path)

    # read conversion table
    extension = os.path.splitext(conversion_table_file_path)[1].upper()
    if extension == '.CSV':
        conversion_table = pd.read_csv(conversion_table_file_path)
    else:
        raise Exception("Conversion table file must be in CSV format.")
    
    # read taret metadata schema
    extension = os.path.splitext(target_schema_file_path)[1].upper()
    if extension == '.JSON':
        with open(target_schema_file_path) as f:
           target_metadata_schema = json.load(f)
    else:
        raise Exception("Target schema file must be in JSON format.")

    converted_metadata = {}

    for original_metadata_item in original_metadata_items:
        
        original_path = original_metadata_item['path']
        converted_paths = lookup_converted_paths(original_path, conversion_table)
        if converted_paths is None:
            continue

        path_no = 0
        while path_no < len(converted_paths):
            converted_path = converted_paths[path_no]
            full_path = converted_path.split('/')
            metadata_item_value = original_metadata_item['value']
            partial_metadata = converted_metadata
            partial_path = []
            upper_array_metadata = None

            for index, element in enumerate(full_path, start=1):
                partial_path.append(element)
                partial_schema = get_partial_schema(target_metadata_schema, partial_path)
                element_type = partial_schema['type']

                if index == len(full_path):

                    if element_type == 'object':
                        raise Exception("Last elememt cannot be an object.")
                    elif element_type == 'array':
                        items_type = partial_schema['items']['type']
                        if items_type == 'boolean':
                            metadata_item_value = True if metadata_item_value == 'true' else False
                        elif items_type == 'integer':
                            metadata_item_value = int(metadata_item_value)
                        elif items_type == 'number':
                            metadata_item_value = float(metadata_item_value)

                        if element not in partial_metadata:
                            partial_metadata[element] = []
                            partial_metadata[element].append(metadata_item_value)
                        else:
                            partial_metadata[element].append(metadata_item_value)
                    else:
                        if element not in partial_metadata:
                            if element_type == 'boolean':
                                metadata_item_value = True if metadata_item_value == 'true' else False
                            elif element_type == 'integer':
                                metadata_item_value = int(metadata_item_value)
                            elif element_type == 'number':
                                metadata_item_value = float(metadata_item_value)

                            partial_metadata[element] = metadata_item_value
                        else:
                            upper_array_metadata.append({})
                            path_no = path_no - 1
                            break
                else:
                    if element_type == 'object':
                        if element not in partial_metadata:
                            partial_metadata[element] = {}
                            partial_metadata = partial_metadata[element]
                        else:
                            partial_metadata = partial_metadata[element]
                    elif element_type == 'array':
                        if element not in partial_metadata:
                            partial_metadata[element] = []
                            partial_metadata[element].append({})
                            upper_array_metadata = partial_metadata[element]
                            partial_metadata = partial_metadata[element][0]
                        else:
                            upper_array_metadata = partial_metadata[element]
                            partial_metadata = partial_metadata[element][-1]
                    else:
                        raise Exception("An element must be either object or array except for the last element.")
                
            path_no = path_no + 1

    return converted_metadata
            