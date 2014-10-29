# Climate - Elevation

## Climate.csv

### Description
IEDC Climate indicators for BC Census Subdivisions - temperature and precipitation. Values are for the reference points associated with each Census Subdivision.  Data are taken from ClimateBC for the reference normal period 1981-2010.

### Source
ClimateBC v5.03 - http://cfcg.forestry.ubc.ca/projects/climate-data/climatebcwna/

### Caveats etc
See ClimateBC web site for details on the source data.
Interpreting the snowfall numbers as cm is an approximation - the unit provided is mm of precipitation, but 1cm snow per 1mm of precipitation is accepted as a general rule of thumb.

### Preparation notes
- download ClimateBC v5.03 application from http://cfcg.forestry.ubc.ca/projects/climate-data/climatebcwna/
- create required .csv input file holding lat/long of all communities (lat/long is from reference point locations for Census Subdivisions - from StatsCan, provided by GeoBC - see http://www.statcan.gc.ca/pub/92-195-x/2011001/other-autre/point/point-eng.htm)
- run ClimateBC (multi-location interface):
    - input: communities.csv 
    - climate source:  Normals 1981-2010
    - variables:  All Variables
- pull out desired fields from resulting csv
- rename fields as necessary
- add field MAR (mean annual rain) and calculate it as Mean annual precipitation minus Annual avg snowfall (MAR = MAP - PAS)


## Elevation.csv

### Description
Elevation statistics (in meters) for BC Census Subdivisions. Values are derived from the Provincial Digital Elevation Model (DEM).
Negative elevation values indicate an area below sea level. 

### Source
BC TRIM 1:20,000 DEM, 25m resolution  
http://geobc.gov.bc.ca/base-mapping/imagery/products/gridded.html

### Caveats etc
Values are based entirely on the Digital Elevation Model.

### Preparation notes
- create a provincial mosaic of 1:250,000 BC DEM tiles
- create required .csv input file holding lat/long of all communities (lat/long is from reference point locations for Census Subdivisions - from StatsCan, provided by GeoBC - see http://www.statcan.gc.ca/pub/92-195-x/2011001/other-autre/point/point-eng.htm)
- calculate elevation at each point using zonal_stats tool in python-raster-stats https://github.com/perrygeo/python-raster-stats
- calculate elevation maximum, minimum, mean within each Census Subdivision (CSD) polygon by using CSD polygons as the input to the zonal_stats
- join point and polygon output files and rename columns as required