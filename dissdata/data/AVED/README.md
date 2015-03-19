# econ_whse_post_secondary_clusters_bc
- copied enrollment/grad data from provided spreadsheet
- added columns from provided logfile
- populated ids linking to institutions table

# econ_whse_post_secondary_instttns_bc
- pulled institutions in clusters file from file provided by Mike
- pulled POST_SECONDARY_EDUC_ID ids from list provided by Mike for Main Campuses
- get location of institutions by joining back to source points
```
SELECT 
  p.post_secondary_educ_id,
  p.institution_name,
  csd.census_subdivision_id,
  csd.census_subdivision_name
FROM 
  whse_imagery_and_basemaps.gsr_post_secondary_educ_isp p
INNER JOIN mit.cen_census_subdivisions csd 
ON st_within(p.geom, csd.geom)
WHERE post_secondary_educ_id IN (9,17,22,31,43,49,54,57,65,70,71,77,87,105,114,121,125,131,139,142,145,154,157,159,164)
ORDER BY post_secondary_educ_id
```
- manually dumped results into spreadsheet and added research inst manually too