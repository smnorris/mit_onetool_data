# network_coverage.csv

## Title
BC Network Interaction, by Census Subdivision

## Description
This dataset contains network connectivity by technology service type within the Census Subdivisions of the Province of British Columbia.  The table was derived from an overlay of BCNC_BC_NETWORK_COVERAGE_SP and CEN_CENSUS_SUBDIVISIONS. The percentage network cover was derived for each census subdivision based on overlap with the network coverage layer.

## Source
BCNC_BC_NETWORK_COVERAGE_SP
https://apps.gov.bc.ca/pub/geometadata/metadataDetail.do?recordUID=63740&recordSet=ISO19115

## Caveats etc
This is an approximation only.

## Preparation notes
- Overlay source layers with GIS package:
  + hex bin layer (bcnc_bc_network_coverage_sp) 
  + census subdivisions (cen_census_subdivisions)
- Load resulting table to db
- Run query `src\network_bc.sql`, dump to output to csv
- for more info, see the documentation provided in the March 2014 delivery file