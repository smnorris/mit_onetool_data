# first_nations_population.csv

## Title
BC First Nation Community name(s), location, and population.

## Description
A list of British Columbia First Nations communities, including
- primary name(s)
- associated Nation
- location (by matching to Census Subdivision or Canada Lands Administrative Boundary (CLAB) ID)
- population, broken down by
  + number of individuals registered with the First Nation and living on reserve or Crown lands
  + number of individuals registered with the First Nation and living off reserve or Crown lands

## Sources
First Nation names were provided by BC Ministry of Aboriginal Relations and Reconiliation.

Population was provided by Aboriginal Affairs and Northern Development Canada via INSTAT (Infopubs@aadnc-aandc.gc.ca).

Locations were derived by linking the Population and Names files to Statistics Canada Census Subdivisions via the First Nation community point locations available from the First Nations Economic Development Database (www.fnedd.ca)

## Caveats etc
INSTAT provided an Excel file containing Indian Register data for the 198 First Nations administered by our BC Regional Office broken down by residency and gender.  These counts were extracted directly from AANDC's Indian Registration System (IRS) as at December 31, 2014, and have not been adjusted for late reporting of births or deaths.  Furthermore, they reflect residency codes for individuals affiliated with these First Nations only.  As such, on reserve numbers for each First Nation should not be taken to represent the true population for the following reasons:
 
1) They contain no information on any Non-Registered individuals who may be living on reserve or crown lands, and
 
2) similarly, they contain no information on any members registered to other First Nations who may be living on reserve or crown lands, and
 
3) because "On Reserve & On Crown Land" is a roll-up of residency fields 1 through 5, they may include counts pertaining to registrants residing on reserve or crown lands belonging to other First Nations.
 
For purposes of the Privacy Act, and to minimize the risk of identifying individuals, we have worked some safeguards into the data.  All data for First Nations with less than 40 registrants have been suppressed.  Furthermore, individual cells with a value of less than 10 have been suppressed as well as adjacent cells to guard against residual disclosure.
 
 
Limitations on IR Data
 
An individual's information on the IRS is usually updated on the reporting of a life event to the First Nation's Indian Registry Administrator (IRA), although some bands may update the system more frequently.  Perhaps the greatest limitation on Indian Register data involves the late reporting of these life events.
 
According to recent history, about 70% of all births reported in any particular year actually occurred in a prior year.  This is not out of the ordinary since it is common practice for children to be registered between the ages of 1 to 5.  Besides births, individuals can remain on the Indian Register for some time after they are deceased.  A certificate of death or a confirmation of presumed death is normally required to remove a name from the system.
 
A second major limitation involves residency codes.  Similar to life events, residency codes tend to be updated by the IRA when a life event is reported (although some bands may again update the system more frequently).  This makes it possible for an individual to move back and forth between on and off reserve, and never have his/her information updated if a life event was not reported.

## Preparation notes

FN Name, Population and location had to be linked, each is from a different data source.

1. Receive list of FNs from MARR, population numbers from AANDC/INSTAT (including Yukon FNs), download IR locations from FNEDD (https://www.fnedd.ca/)

2. Manually transfer each dataset to a clean .csv file and load each to postgres.
    - `population.csv`
    - `names.csv`
    - `fnedd.csv`

3. Full outer join all source data as best as possible, and also spatially join to CSD polygons, WHSE_ADMIN_BOUNDARIES.CLAB_INDIAN_RESERVES, and GeoBC tir_bc polygons. This was an iterative process over several months, no clean code was produced. Rough queries are available on request.

4. Manually fix and QA unmatched records. Primary issues were:
    - FNEDD points not within CSDs defined as IRs, and no matching IR nearby - FN was assigned a CLAB_ID in these cases (4)
    - FNEDD points not within CSDs defined as IRs, matching IR nearby - FN was manually matched to appropriate CSD
    - name mismatches preventing join - matches were made manually  

    Where matches were outside of BC or otherwise complicated, notes were made in the Notes column.

5. Add Nation column, populate with values from FNEDD data
6. Split data into multiple tables, adding official `band_name` for reference in population table
