# Population Projections

## population_projections.csv

### Title
Regional District Population Projections, P.E.O.P.L.E. 2014 (Sep 2014)

### Description
A population projection is a forecast of future population growth. BC Stats applies the Component/Cohort-Survival method to project the population. This method "grows" the population from the latest base year estimate by forecasting births, deaths and migration by age. These forecasts are based on past trends modified to account for possible future changes and, consequently, should be viewed as only one possible scenario of future population.

B.C. level projections are usually updated in January or February each year, with sub-provincial projections following a few months after. All population estimates and projections are as of July 1st.

### Source
http://www.bcstats.gov.bc.ca/StatisticsBySubject/Demography/PopulationProjections.aspx

### Caveats etc
For more information contact Werner Grundlingh 250-387-8896

### Preparation notes
- downloaded csv from source noted, using these options
    + region type: Regional District
    + regions(s): all
    + year(s): 2012+
    + sex(es): Totals
    + age group: 5-Year Age Groups
- removed provincial totals
- removed Gender column
- removed regional district code column
- change age group column names, prefixing with 'pop'
- change year column to 'projection_year'
- join to census subdivisions (cd.csv) on name, adding census_division_id column
  `$ csvjoin -c "CENSUS_DIVISION_NAME,regional_district" --outer cd.csv Population_Projections.csv > pop_projections.csv`
- manually fix unmatched records (only Kootenay Boundary didn't exactly match)
    