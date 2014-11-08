# Climate.csv

## Title
Climate statistics for BC Census Subdivisions

## Description
IEDC Climate indicators for BC Census Subdivisions - temperature and precipitation. Values are for the reference points associated with each Census Subdivision.  Data are taken from ClimateBC for the reference normal period 1981-2010.

## Source
ClimateBC v5.03 - http://cfcg.forestry.ubc.ca/projects/climate-data/climatebcwna/

## Caveats etc
See ClimateBC web site for details on the source data.
Interpreting the snowfall numbers as cm is an approximation - the unit provided is mm of precipitation, but 1cm snow per 1mm of precipitation is accepted as a general rule of thumb.

## Preparation notes
- download ClimateBC v5.03 application from http://cfcg.forestry.ubc.ca/projects/climate-data/climatebcwna/
- create required .csv input file holding lat/long of all communities (lat/long is from reference point locations for Census Subdivisions - from StatsCan, provided by GeoBC - see http://www.statcan.gc.ca/pub/92-195-x/2011001/other-autre/point/point-eng.htm)
- run ClimateBC (multi-location interface):
    - input: communities.csv
    - climate source:  Normals 1981-2010
    - variables:  All Variables
- pull out desired fields from resulting csv
- rename fields as necessary
- add field MAR (mean annual rain) and calculate it as Mean annual precipitation minus Annual avg snowfall (MAR = MAP - PAS)
