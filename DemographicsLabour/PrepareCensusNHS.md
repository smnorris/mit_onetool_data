# Prepare StatsCan 2011 Census and NHS data

## Download source data (census subdivision level)

### Census Profiles
Get Census profile data:
```
$ curl -O http://www12.statcan.gc.ca/census-recensement/2011/dp-pd/prof/details/download-telecharger/comprehensive/comp_download.cfm?LANG=E&CTLG=98-316-XWE2011001&FMT=CSV301
```

### NHS Profiles
As of writing, data.gc.ca only provides NHS data as [xml](http://data.gc.ca/data/en/dataset/219ba84b-07ae-4ae0-bf90-67d0a7544272).
CSV files are easier to deal with and available using the form [here](http://www12.statcan.gc.ca/nhs-enm/2011/dp-pd/prof/details/download-telecharger/comprehensive/comp-csv-tab-nhs-enm.cfm?Lang=E)

## Examine the data and extract BC

After unzipping, we see:

- the Census data is held in a single national csv, prefixed by 98
- The NHS census data is already broken up by province, each file prefixed by 99, with abbreviated province name as suffix

Using the usual desktop tools to examine and clean these files won't work, they are too big, especially the census file: my copy of Excel 2003 will choke or only load a portion, and Google Refine says 1hr to load.  

Examine and filter the data with command line tools instead:

`head` shows us what the census file looks like
```
$ head 98*CSV -n 5
Census Profile - Census Subdivisions (CSDs)
Geo_Code,Prov_Name,CD_Name,CSD_Name,CSD_Type,Topic,Characteristics,Note,Total,Flag_Total,Male,Flag_Male,Female,Flag_Female
1001101,Newfoundland and Labrador,Division No.  1,"Division No.  1, Subd. V",Subdivision of unorganized,Population and dwelling counts,Population in 2011,1,62,,,...,,...
1001101,Newfoundland and Labrador,Division No.  1,"Division No.  1, Subd. V",Subdivision of unorganized,Population and dwelling counts,Population in 2006,1,65,,,...,,...
1001101,Newfoundland and Labrador,Division No.  1,"Division No.  1, Subd. V",Subdivision of unorganized,Population and dwelling counts,2006 to 2011 population change (%),,-4.6,,,...,,...
```

As first line isn't the header, remove using tail:

```
$ tail 98*.CSV -n +2 > t.csv
```

Pull out BC data using the [csvkit tools](http://csvkit.readthedocs.org/en/latest/), noting that the file encoding must be specified:

```
$ pip install csvkit # (if not already installed)
$ csvgrep -e iso-8859-1 -c 2 -m "British Columbia" t.csv > census.csv
```

Now take a look at NHS data, at csd level:
```
$ csvcut -n -e iso-8859-1 99-004-XWE2011001-301-BC.csv
  1: Geo_Code
  2: Prov_Name
  3: CD_Name
  4: CSD_Name
  5: CSD_type
  6: GNR
  7: Topic
  8: Characteristic
  9: Note
 10: Total
 11: Flag_Total
 12: Male
 13: Flag_Male
 14: Female
 15: Flag_Female
```

Unfortunately the combination of Topic and Characteristic isn't unique within the NHS data (for example, there is no way to distinguish between total income categories and after tax income categories). We'll need to post process the data and either change the topic value or add another column. To do that requires that the data stays ordered, so lets add a line number to the file to make sure nothing gets out of order in the db.
```
$ csvgrep -e iso-8859-1 -c 2 -m "British Columbia" -l 99-004-XWE2011001-301-BC.csv > nhs_csd.csv
```

Now, look at the NHS data at CA/CMA level.
```
$ head -n 3 99*201.csv
National Household Survey - Census Metropolitan Areas (CMAs) and Census Agglomerations (CAs)
Geo_Code,Prov_Name,CMA_CA_Name,Geo_Type,GNR,Topic,Characteristic,Note,Total,Flag_Total,Male,Flag_Male,Female,Flag_Female
001,Newfoundland and Labrador,St. John's,CMA,27.5,Citizenship,Total population in private households by citizenship,1,193830,,93615,,100210,
```
Same problem as census file, get rid of the first line.
```
$ tail 99*201.csv -n +2 > t.csv
```
But csvkit tools aren't working. Unfortunately the notes are included in the csv.
```
$ tail -n 3 99*201.csv
How to cite: Statistics Canada. 2013. National Household Survey Profile. 2011 National Household Survey.
Statistics Canada Catalogue no. 99-004-XWE. Ottawa. Released September 11 2013.
http://www12.statcan.gc.ca/nhs-enm/2011/dp-pd/prof/index.cfm?Lang=E
```
With further investigation this starts 165 lines from the bottom.
Find how many lines there are in the file and just keep the top.
```
$ cat t.csv | wc -l
148006
$ head -n 147842 t.csv > t2.csv
```
csvkit tools now work fine.
```
$ csvgrep -e iso-8859-1 -c 2 -m "British Columbia" -l t2.csv > nhs_cma.csv
```
Same deal if using the 'Federal electoral districts' or 'Census Divisions' files. I'm sure this could be done in a one liner with no intermediate files...
```
$ tail 99*501.csv -n +2 > t.csv
$ cat t.csv | wc -l
295846
$ head -n 295681 t.csv > t2.csv
$ csvgrep -e iso-8859-1 -c 2 -m "British Columbia" -l t2.csv > nhs_fed.csv
$ tail 99*701.csv -n +2 > t.csv
$ cat t.csv | wc -l
281446
$ head -n 281281 t.csv > t2.csv
$ csvgrep -e iso-8859-1 -c 2 -m "British Columbia" -l t2.csv > nhs_cd.csv
```
Note that the CD file isn't quite standard - the Geo_Code column is noted as Geo_code. I just opened up the file in sublime and edited that line.

## Load data to postgres
Load the resulting files to a fresh schema in postgres. csvkit does this nicely (although annoyingly there seems to be no option for making columns lower case and I'd rather not bother touching the source columns). Note the encoding for the NHS file that hasn't already been converted to utf8.  

```
$ csvsql --db postgresql://postgres:postgres@localhost:5432/postgis --table census_src --insert census.csv --db-schema mit
$ csvsql --db postgresql://postgres:postgres@localhost:5432/postgis --table nhs_src --insert nhs_csd.csv --db-schema mit
$ csvsql --db postgresql://postgres:postgres@localhost:5432/postgis --table nhs_cma_src --insert nhs_cma.csv --db-schema mit
$ csvsql --db postgresql://postgres:postgres@localhost:5432/postgis --table nhs_fed_src --insert nhs_fed.csv --db-schema mit
$ csvsql --db postgresql://postgres:postgres@localhost:5432/postgis --table nhs_cd_src --insert nhs_cd.csv --db-schema mit
```
Also load spatial data to postgres. A .gdb was provided by GeoBC (Natalie Work) that defines the various geographical boundaries. Load csd and cd tables to the same postgres schema.

## Process the data in postgres to match MIT requirements
This is scripted in `src\ProcessStatsCanData.py`
Output tables are
- demographics_labour_csd
- demographics_labour_cd
Output tables manually copied to csv, slight reordering, renaming of columns.
