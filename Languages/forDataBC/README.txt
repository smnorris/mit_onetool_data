# Languages

## languages.csv

### Title
Census Subdivisions - language spoken most often at home

### Description
For Statistics Canada 2011 Census Subdivisions, total count of language spoken most often at home, taken from the universe of total population (see Caveats) excluding institutional residents.

### Source
Statistics Canada Census Profiles  
http://www12.statcan.gc.ca/census-recensement/2011/dp-pd/prof/details/download-telecharger/comprehensive/comp_download.cfm?LANG=E&CTLG=98-316-XWE2011001&FMT=CSV301

### Caveats etc
The population excluding institutional residents includes Canadian citizens (by birth or by naturalization) and landed immigrants (permanent residents) excluding those who live in institutions (institutional collective dwellings). Canadian citizens and landed immigrants either: (1) have a usual place of residence in Canada; (2) are abroad either on a military base or attached to a diplomatic mission; or (3) are at sea or in port aboard merchant vessels under Canadian registry or Canadian government vessels. Since 1991, the target population also includes persons with a usual place of residence in Canada who are claiming refugee status, who hold study permits, or who hold work permits, as well as family members living with them; for census purposes, this group is referred to as non-permanent residents. The population universe does not include foreign residents.

See http://www12.statcan.gc.ca/census-recensement/2011/dp-pd/prof/help-aide/help-aide.cfm?Lang=E for more info.

Note that some output values are NULL - this is for CSDs where data is supresessed, excluded or not available for various reasons. Join census_subdivision_id to the demographics table to determine if a CSD is flagged.

### Preparation notes
- download file noted in Source above (same source as Demographics and Labour)
- remove first line from file, extract just BC records, encode as utf-8, load to database  
```
$ tail 98*.CSV -n +2 > t.csv  
$ csvgrep -e iso-8859-1 -c 2 -m "British Columbia" t.csv > census.csv
$ csvsql --db postgresql://postgres:postgres@localhost:5432/postgis --table census_src --insert census.csv --db-schema mitdataprep
```
- determine languages to be retained by 
    - create list of languages reported on for BC in existing Community Profiles application (download list from https://tools.britishcolumbia.ca/Invest/Pages/Profile.aspx?page=5&pCommunityID=562&type=1)
    - save list as `languages_cp.csv`, stripping out population values
- extract complete list of languages available form Census, dump to `languages_src.csv`
```
SELECT DISTINCT
 src."Characteristics" AS language
FROM mitdataprep.census_src src
WHERE "Topic" = 'Detailed language spoken most often at home'
```
- compare the two lists of languages
```
$ csvjoin -c "language,LANGUAGE" --outer languages_src.csv languages_cp.csv > languages_join.csv
```
- the match is good, use the list of languages from community profiles in a query that pulls all data from source, saving output as languages.csv

```
-- build the final totals
SELECT
 census_subdivision_id AS "CENSUS_SUBDIVISION_ID", 
 language AS "LANGUAGE",
 SUM(total) AS "COUNT_SPOKEN_AT_HOME"
FROM 

( 
-- extract just the languages of interest
-- some fine detail is lost with 'other official language' combined with English/French but we won't fret about that
SELECT 
 census_subdivision_id, 
 census_subdivision_name,
 CASE 
  WHEN language IN ('Arabic','Mandarin','Cantonese','Chinese, n.o.s','Croatian','Czech','Dutch','English','Finnish','French','German','Greek','Hindi','Hungarian','Ilocano','Italian','Japanese','Korean','Malay','Panjabi (Punjabi)','Persian (Farsi)','Polish','Portuguese','Romanian','Russian','Serbian','Spanish','Tagalog (Pilipino, Filipino)','Tamil','Ukrainian','Vietnamese')
  THEN language
  WHEN language = 'English and non-official language' 
  THEN 'English'
  WHEN language = 'French and non-official language' 
  THEN 'French'
  WHEN language IN ('English and French', 'English, French and non-official language')
  THEN 'English and French'
  ELSE 'Other non-official language'
 END AS language,
 total
FROM 

(
-- extract Topic we are interested in, clean column names, remove subtotal rows
SELECT 
 src."Geo_Code" census_subdivision_id, 
 src."CSD_Name" AS census_subdivision_name,
 src."Characteristics" AS language,
 src."Total" AS total
FROM mitdataprep.census_src src
WHERE "Topic" = 'Detailed language spoken most often at home'
AND "Characteristics" NOT IN 
  ('Detailed language spoken most often at home - Total population excluding institutional residents', 
   'Single responses', 
   'Non-official languages', 
   'Selected Aboriginal languages', 
   'Selected non-Aboriginal languages',
   'Multiple responses')
ORDER BY "Geo_Code", "Characteristics" ) AS subquery1
) AS subquery2
GROUP BY census_subdivision_id, language
ORDER BY census_subdivision_id, language
```
