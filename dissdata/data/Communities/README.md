# communities.csv

## Title
A list of communities used in MIT's DISS application

## Description
MIT's DSS applicatin is to report on a collection of communities/geographical areas.  defined as  Census Subdivisions (municipalities), First Nations, Census Divisions (Regional Districts) and Economic Regions.

## Source
Statistics Canada census geographies via GeoBC

## Caveats etc

## Licence

## Preparation notes
- received list of communities to be used from MIT (Sue) as xls 
- converted to .csv and compared to census subdivisions from GeoBC .gdb (dumped to csv as well)
  `$ csvjoin --outer -c name,CENSUS_SUBDIVISION_NAME communities_from_sue.csv csd.csv > csd_qa.csv`
- manually fixed mismatched records due to typos
- two identified communities have no exact match in the CSD data
    + Jumbo Glacier (it was created after the 2011 Census, and nobody lives there yet anyway)
    + Islands Trust - this is more problematic, and appears to involve grouping several RD electoral area CSDs into a single 'community'. 
    Nope. they are designated places: http://www12.statcan.gc.ca/census-recensement/2011/ref/dict/geo018-eng.cfm

Islands Trust, designated places
- download designated places 
    + geography http://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/bound-limit-2011-eng.cfm
    + Census profile (no NHS available) http://www12.statcan.gc.ca/census-recensement/2011/dp-pd/prof/details/download-telecharger/comprehensive/comp-csv-tab-dwnld-tlchrgr.cfm?Lang=E#tabs2011

These are the relevant designated places in the geography file:
```
$ dumpcsv gdpl000a11a_e.shp -l gdpl000a11a_e | csvgrep -e iso-8859-1 -c 2 -m "Island Trust Area" | csvsort -c 2 | csvcut -c 1,2
DPLUID,DPLNAME
590002,Denman Island Trust Area
590003,Gabriola Island Trust Area part A
590232,Gabriola Island Trust Area part B
590233,Gabriola Island Trust Area part C
590004,Galiano Island Trust Area
590249,Gambier Island Trust Area part A
590250,Gambier Island Trust Area part B
590251,Gambier Island Trust Area part C
590252,Gambier Island Trust Area part D
590253,Gambier Island Trust Area part E
590006,Hornby Island Trust Area
590007,Lasqueti Island Trust Area
590008,Mayne Island Trust Area
590009,North Pender Island Trust Area
590234,Saltspring Island Trust Area part A
590235,Saltspring Island Trust Area part B
590236,Saltspring Island Trust Area part C
590237,Saltspring Island Trust Area part D
590238,Saltspring Island Trust Area part E
590239,Saltspring Island Trust Area part F
590241,Saltspring Island Trust Area part H
590011,Saturna Island Trust Area
590013,South Pender Island Trust Area
590012,Thetis Island Trust Area part A
590248,Thetis Island Trust Area part B
```
extract them:
`$ ogr2ogr -where "DPLNAME like '%Island Trust Area%'" islands_trust.shp gdp*shp`



