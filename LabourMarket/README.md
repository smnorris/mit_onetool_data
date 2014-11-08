# JTST_CENSUS_geographies_xref.csv

## Title
Cross reference between JTST geographies and Census geographies

## Description
Provide a link from JTST regions and economic development regions - JTST does not report on all regions separately

## Source
JTST, Statistics Canada

## Caveats etc
na

### Preparation notes
- manually extracted all JTST regions, all census economic development regions
- manually prepared the table, linking JTST North Coast/Nechako region to the individual Census regions


# lmsm_regional_3digitnoc.csv

## Title
Labour Market Outlook 2010-2020

## Description
Reports on future supply, demand and supply-demand balance for occupations across BC's development regions. The report provides projections to identify occupations in BC at various skill levels that may face shortages of workers. 

## Source
Ministry of Jobs, Tourism and Skills Training

## Caveats etc
Contact JTST for more information.

## Preparation notes
- downloaded file `Labour-Market-Outlook-Regional-Data-by-3-digit-NOC-2010-2020.csv` from DataBC catalog
- downloaded file `Labour-Market-Outlook_DataDictionary.txt` from DataBC catalog
- manually added and populated `jtst_geography_id` column based on region names (note that this is preliminary, see the notes for unemployment above on how jtst_geography_id is assigned)
- minor renaming of other columns in the data file
- created `lmsm_regional_3digitnoc_METADATA.csv` documenting data structure/values based on the information in file `Labour-Market-Outlook_DataDictionary.txt`
- note that a geographic ID of 6 is given for British Columbia, but I'm not sure that there is a corresponding geographic record in the census data published to BCGW


# unemployment.csv

## Title
Unemployment by Economic Region

## Description
*require JTST input*

## Source
JTST, Statistics Canada

## Caveats etc
*require JTST input*

### Preparation notes
- received file `WorkBC Navigator September 2014.xlsx` from Nick Bystedt (JTST)
- extracted unemployment data for economic regions and CMAs to new .csv file
- added and populated jtst_geography_id column, giving Nechako/North Coast an id of 5965 
- created the lookup/cross-ref table `JTST_CENSUS_geographies_xref.csv` for mapping JTST regions to CENSUS regions. Assigning `5965` to both North Coast and Nechacko regions seems reasonable at first glance. there is not a conflict with any other geography (based on a check here: http://www12.statcan.gc.ca/census-recensement/2011/dp-pd/prof/index.cfm?Lang=E). Another possibility is to use JTST internal IDs for all regions (if they exist)
- added unemployment_y1 and unemployment_y2 columns, populated with data from forecasts for 2015, 2016
- note that unemployment forecasts are only available at the economic region level
- note that a geographic ID of 6 is given for British Columbia, but I'm not sure that there is a corresponding geographic record in the census data published to BCGW
