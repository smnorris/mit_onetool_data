# origin_destination_csd.csv

## Title
A listing of distances and travel times between communities and common destinations

## Description
Distance and travel times between communities (census subdivisions) and destinations such as major centers, airports, ports, post-secondary institutions. This information permits querying of the closest of these destinations to a given community.

## Source
Open Street Map via MapQuest's Open Directions API (http://open.mapquestapi.com/directions/)

## Caveats etc
See terms of use here: http://developer.mapquest.com/web/info/terms-of-use

## Preparation notes (prelminary)
- build a .csv table of origins, which is all incorporated census subdivisions with lat/lon by extracting from StatsCan reference points (`src/csd_locations`)
- copy csd_locations.csv to destinations_src.csv
- add columns identifying one of (major centre, airport/port, post-sec institution)
- populate major centre and airport/port manually
- load to postgres
- populate postsec_inst column with this query:
```
    UPDATE onetool.destinations
    SET postsec_inst = 'T'
    WHERE csd_uid IN 
    (
    SELECT DISTINCT
      csd.census_subdivision_id::int
    FROM 
    whse_human_cultural_economic.cen_census_subdivisions csd
    INNER JOIN
    whse_imagery_and_basemaps.gsr_post_secondary_educ_isp aved
    ON ST_Intersects(csd.geom, aved.geom)
    ORDER BY census_subdivision_id
    ) 
```
- extract just records that are destinations, dump to new csv (destinations.csv)