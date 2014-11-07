# Building origin-destination table

Compile distances between origin and destination communities using MapQuest's Open Directions API (http://open.mapquestapi.com/directions/)

## Origins
Origins are the complete list of Census Subdivisions (csd_locations.csv), location is the 'Reference Point' coordinate provided by StatsCan.

## Destinations
Destinations required by onetool are communities with an:
  - airport (regional and international)
  - port
  - post-secondary institution

To determine which communities have each of these features, several steps were taken:

- airport and port features were taken from 2012 Community Profiles mapping (compiled by Hillcrest Geographics from federal listings) and loaded to postgres schema onetool
`$ gdb2pg source_data.gdb`


