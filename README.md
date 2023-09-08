## Geospatial Metadata Toolkit (GeoMetaTool)

The Geospatial Metadata Toolkit is a Python package designed to streamline geospatial metadata operations. Whether you're working with GIS data, satellite imagery, or any other geospatial information, GeoMetaTool provides a convenient set of tools for three primary tasks: **metadata extraction**, **metadata conversion**, and **metadata validation**.

### Metadata extraction
GeoMetaTool simplifies the process of extracting essential metadata from various types of geospatial data. It allows you to access key information about spatial datasets, including details such as coordinate reference systems, temporal extents, data sources, and more. With this feature, you can save time and avoid the hassle of manually retrieving metadata from your geospatial assets. Specifically, it extract geospatial metadata in ISO 19115-3 format embedding ISO 19110 as the contentInfo element.

The package is currently under development to support the following geospatial data
* Vector: shp, kml, mif, gml, dxf, geojson
* Raster: tif, tiff
* Collection: gdb, gpkg

```sh
import geometatool
iso_metadata = geometatool.extract_metadata(input_file_path, default_metadata_values=[])
iso_metadata.save_to_file(output_file_path)
```

### Metadata conversion
Dealing with different metadata standards across geospatial projects can be cumbersome. GeoMetaTool offers a solution by enabling the conversion of metadata between different schemas. This is achieved through a conversion table between ISO 19115-3/19110 and another predefined schema. This feature promotes interoperability and consistency across diverse geospatial data sources. 

The package is currently under development to support the following geospatial metadata

* XML schema: ISO 19115-3/19110, QGIS metadata
* JSON schema: NADA geospatial, DDH

```sh
import geometatool
converted_metadata = geometatool.convert_metadata(input_file_path, conversion_table_file_path, target_schema_file_path)
with open(output_file_path, "w") as f:
    json.dump(converted_metadata, f, indent = 4)
```

### Metadata validation
GeoMetaTool allows you to validate the correctness of metadata syntax, ensuring that your geospatial metadata adheres to ISO 19115-2/19110 or predefined json schema.

```sh
import geometatool

geometatool.validate_xml_ISO19115_3(instance_file_path)
# The XML is well formed.
# The instance is valid aginst the ISO 19115-3 and ISO 19110 schemas.

geometatool.validate_json(instance_file_path, schema_file_path)
# The instance is valid aginst the provided schema.
```

