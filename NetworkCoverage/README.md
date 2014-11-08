# Network Coverage

## network_coverage.csv

### Title
BC Network Interaction, by Census Subdivision

### Description
This dataset contains network connectivity by technology service type within the Census Subdivisions of the Province of British Columbia.  The table was derived from an overlay of BCNC_BC_NETWORK_COVERAGE_SP and CEN_CENSUS_SUBDIVISIONS. The percentage network cover was derived for each census subdivision based on overlap with the network coverage layer.

### Source
BCNC_BC_NETWORK_COVERAGE_SP

### Caveats etc

### Preparation notes
- Overlay source layers with GIS package:
  + hex bin layer (bcnc_bc_network_coverage_sp) 
  + census subdivisions (cen_census_subdivisions)
- Load resulting table to db
- Run query `src\network_bc.sql`, output is telecommunications_csd
- Dump to csv