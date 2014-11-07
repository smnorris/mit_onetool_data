README.md

Processes for processing Network BC network coverage hex bins.

1. Overlay source layers with GIS package to produce network_csd layer
  - hex bin layer (bcnc_bc_network_coverage_sp) 
  - census subdivisions (cen_census_subdivisions)
2. Load resulting network_csd layer to db
3. Run query network_bc.sql, output is telecommunications_csd
4. Dump to csv