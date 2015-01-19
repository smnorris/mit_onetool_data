# Railway.csv

## Title
Railway service for BC Census Subdivisions

## Description
Railway service information for BC Census Subdivisions

## Source
National Rail Network

## Caveats etc


## Preparation notes
- source track layer projected into BC Albers and loaded to postgres
``` 
ogr2ogr -f PostgreSQL PG:'host=localhost user=postgres dbname=postgis password=postgres port=5432' -lco OVERWRITE=YES -t_srs EPSG:3005 -lco SCHEMA=temp -lco GEOMETRY_NAME=geom -nln nrn -nlt PROMOTE_TO_MULTI NRN.shp
```
