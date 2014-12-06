# econ_whse_energy_utilities_bc.csv

## Title
Electrical utilities that serve British Columbia municipalities.
Utility name, url and sample average rate charges ($/kWh) at small, medium and large levels.

## Description
A list of British Columbia electrical utilities and sample average rate charges ($/kWh) at small, medium and large levels.

## Source
List of utilities is from http://www.bcuc.com/Documents/MiscDocs/Regulated_Utilities.pdf. 
To be included, utilities must
- be electrical or natural gas (propane grids are not included)
- serve incorporated areas
- not serve only individual developments (such as River District Energy Limited Partnership, Dockside Green Energy LLP)

Note that the list from BCUC is no longer current, Kelowna does not run a utility anymore, Fortis now serves Kelowna - http://www.kelowna.ca/CM/Page391.aspx)

Also note that according to FortisBC, all Fortis utilities are merging as of Jan01 2015 - therefore only a single record is included for Fortis.

For sources of rate information, see datafile for links

## Caveats etc
All rate information is current as of December 01 2014 and subject to change.
Use rate info with caution - average rates are approximations based on interpretation of several sources. Users should check with the individual utility for quotes at required service level.

## Preparation notes
- manually compile a list of utilities and web sites as per Source above
- manually compile electrical rates at given service levels by interpreting various rate schedules. Use rate info with caution.
- manually compile natural gas rates by interpreting various rate schedules. Note that charges are averages for various service areas and include delivery charges.


# econ_whse_telecom_bc.ca

## Title
A list of selected telecommunications companies serving BC municipalities.

## Description
A list of selected telecommunications companies serving BC municipalities.

## Source
Telecom company names and addresses taken from their internet sites and existing Community Profiles data.

## Caveats etc
This list is not comprehensive

## Preparation notes
Data taken from various telecom web sites and MIT Community Profiles. (community profiles data verified by internet search)


# econ_whse_utility_telecom_service_areas_bc.csv

## Title
A list identifying which utilities serve which BC municipalities.

## Description
For each municipality, lists electrical, natural gas, telecommunications companies that serve the municipality.

## Source
List of municipalities is from 2011 census subdivisions, plus Jumbo Glacier 

## Caveats etc
Use the service area lists for general information only. This should not be used for site specific planning. Contact individual utilities/companies for more detailed information.

## Preparation notes
- take list of communities from census subdivisions .gdb, extracting only municipalities
- add Jumbo Glacier
- use BC Hydro and Fortis online service area maps as general guides
- download utility data from ici society ftp site (ftp geoshare.icisociety.ca), contact Steve Mark for access credentials
- extract utility .gdbs for Fortis areas, where there are Fortis DIST_POLE features in a given community, presume that it is a Fortis electrical area (unless the community has its own utility)
- load fortis distribution_pipe layer to postgis
- overlay fortis distribution pipes with communities, presuming that where Fortis has a distribution pipe, it serves the community
```
DROP TABLE IF EXISTS mit.fortis_pipe;

CREATE TABLE mit.fortis_pipe
AS SELECT status, st_simplify(st_transform(geom, 3005), 100) AS geom
FROM mit.distribution_pipe;

SELECT DISTINCT 
  a.census_subdivision_id, 
  a.census_subdivision_name, 
  2 AS gas_utility
FROM 
  mit.cen_census_subdivisions a, 
  mit.fortis_pipe b
WHERE a.census_subdivision_type_code NOT IN ('IRI', 'RDA', 'NL', 'IGD', 'S-E')
AND st_intersects(a.geom, b.geom)
ORDER BY census_subdivision_name;
```
- dump this to .csv, join to utility_service areas table
`csvjoin -c census_subdivision_id --outer econ_whse_energy_utility_service_areas_bc.csv fortis.csv > t.csv`
- manually populate PNG communities based on map: http://www.png.ca/systems-map/
- spot check a few communities with no gas service - Pemberton, Golden, Lions Bay, Lytton, Lillooet - seems correct but points out the inadequacy of Fortis BC online map detail - gas line goes up Indian Arm to Squamish, Lions Bay isn't serviced
- use the same procedure for telus (cable_wire table) and shaw (pole table)
- no telus service for Northern Rockies (Ft Nelson) - it is Northwestel
- for major areas with no Shaw service, used google to determine if there is cable service. Added providers Mascon Cable Systems, Coast Cable, CityWest. There are many more but it is difficult to determine exactly which companies serve which communities. 


