## Geospatial Metadata Toolkit (GeoMetaTool)

The Geospatial Metadata Toolkit is a versatile Python package designed to streamline geospatial metadata operations. Whether you're working with GIS data, satellite imagery, or any other geospatial information, GeoMetaTool provides a convenient set of tools for two primary tasks: **metadata extraction** and **metadata conversion**.

### Metadata extraction
GeoMetaTool simplifies the process of extracting essential metadata from various types of geospatial data. It allows you to effortlessly access key information about spatial datasets, including details such as coordinate reference systems, temporal extents, data sources, and more. With this feature, you can save time and avoid the hassle of manually retrieving metadata from your geospatial assets. Specifically, it extract geospatial metadata in ISO 19115-3 format embedding ISO 19110 as the contentInfo element.

The package is currently under development to support the following geospatial data
* Vector: shp, kml, mif, gml, dxf, geojson
* Raster: tif, tiff
* Collection: gdb, gpkg

```sh
import geometatool
metadata_extractor = geometatool.MetadataExtractor(file_path, default_values)
metadata_extractor.save(output_path)
```

### Metadata conversion
Dealing with different metadata standards across geospatial projects can be cumbersome. GeoMetaTool offers a seamless solution by enabling the conversion of metadata between different standards. This is achieved through a conversion table between ISO 19115-3/19110 and a user-defined schema. This feature promotes interoperability and consistency across diverse geospatial data sources. 

The package is currently under development to support this feature
```sh
import geometatool
metadata_extractor = geometatool.MetadataConverter(...)
metadata_extractor.save(...)
```
