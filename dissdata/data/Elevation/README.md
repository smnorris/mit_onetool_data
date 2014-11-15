# Elevation.csv

## Title
Elevation statistics for BC Census Subdivisions

## Description
Elevation statistics (in meters) for BC Census Subdivisions derived from the BC Digital Elevation Model (DEM).  For each Census Subdivision, point, mean, max, and min elevations are included.  Mean, max, min are calculated for the entire terrestrial portion of each Census Subdivision. Point elevations are for the reference point associated with the Census Subdivision.
Negative elevation values indicate an area below sea level. 

## Source
BC TRIM 1:20,000 DEM, 25m resolution  
http://geobc.gov.bc.ca/base-mapping/imagery/products/gridded.html

## Caveats etc
Values are based entirely on the Digital Elevation Model.

## Preparation notes
- create a provincial mosaic of 1:250,000 BC DEM tiles
- create required .csv input file holding lat/long of all communities (lat/long is from reference point locations for Census Subdivisions - from StatsCan (in GeoSuite), provided by GeoBC - see http://www.statcan.gc.ca/pub/92-195-x/2011001/other-autre/point/point-eng.htm)
- calculate elevation at each point using zonal_stats tool in python-raster-stats https://github.com/perrygeo/python-raster-stats
- calculate elevation maximum, minimum, mean within each Census Subdivision (CSD) polygon by using CSD polygons as the input to the zonal_stats
- join point and polygon output files and rename columns as required
- add reference point lat/lon coordinates as requested by DataBC
- lat/lon data were extracted from a GeoBC provided spreadsheet. The data is also available in GeoSuite2011.mdb file, in the table "CSD", columns REPPOINT_LATITUDE and REPPOINT_LONGITUDE. See 
http://www12.statcan.gc.ca/census-recensement/2011/geo/ref/geosuite-eng.cfm
