# JTST labour market information

## unemployment.csv

### Title
Unemployment by Economic Region

### Description
<TBD>

### Source
JTST, Statistics Canada

### Caveats etc
<TBD>

### Preparation notes
- received file `WorkBC Navigator September 2014.xlsx` from Nick Bystedt (JTST)
- extracted unemployment data for economic regions and CMAs to new .csv file
- added geography_id and geography_name columns, populated geography_id
- split row for Nechako/North Coast into two rows, one for each region (with same value). Note that this not may be the best strategy for dealing with this grouping of regions. A lookup table may be preferred - see preparation nots for lmsm_regional_3digitnoc.csv below
- added unemployment forecasts for 2015,2016
- note that unemployment forecasts are only available at the economic region level
- a geographic ID of 6 is given for British Columbia, but I'm not sure that there is a corresponding geographic record in the census data published to BCGW


## lmsm_regional_3digitnoc.csv

### Title
Labour Market Outlook 2010-2020

### Description
Reports on future supply, demand and supply-demand balance for occupations across BC's development regions. The report provides projections to identify occupations in BC at various skill levels that may face shortages of workers. 

### Source
Ministry of Jobs, Tourism and Skills Training

### Caveats etc
Contact JTST for more information.

### Preparation notes
- downloaded file `Labour-Market-Outlook-Regional-Data-by-3-digit-NOC-2010-2020.csv` from DataBC catalog
- downloaded file `Labour-Market-Outlook_DataDictionary.txt` from DataBC catalog
- manually added and populated `geography_id` column based on region names (note that this is preliminary, the id is a combination for North Coast/Nechacko, see 'Remaining issues' below)
- minor renaming of othere columns in the data file for clarification
- created `lmsm_regional_3digitnoc_METADATA.csv` based on the information in file `Labour-Market-Outlook_DataDictionary.txt`

### Remaining issues
- geographic (economic region) names are not standard
- how to handle North Coast / Nechako combination?
    + duplicate the data, one set for each region?
      This has been my strategy for smaller datasets but it seems impractical to continue given the size of this table
    + create a lookup table mapping JTST regions to economic regions?
      A potential lookup table has been created, see `JTST_regions_xref.csv`. Assigning `5965` to both North Coast and Nechacko regions seems reasonable at first glance, there should not be a conflict with any other geography. Another possibility is to use JTST internal IDs for all regions (if they exist)
- a geographic ID of 6 is given for British Columbia, but I'm not sure that there is a corresponding geographic record in the census data published to BCGW
