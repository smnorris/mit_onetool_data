## Preparation notes

### Receive files

#### Representatives
- FederalGovernment - from Community Profiles, BC profile
- ProvincialGovernment - from Communitiy Profiles, BC profile
- Local Government - from MIT
Rename to `federal.csv`, `provincial.csv`, `municipal.csv`, clean headers manually to match desired output column names, send to postgres (`temp` schema)

#### riding boundaries
Provincial electoral districts from BCGW
Load to postgres `whse_admin_boundaries` schema

Federal electoral districts are from 
http://geogratis.gc.ca/api/en/nrcan-rncan/ess-sst/6d1d8f90-1c25-5fd0-880d-138d27c8cb57.html
Load to `mit` schema after selecting out just BC in ArcMap (loading the full shapefile bailed)

### Check links between datasets

Provincial boundaries to riding table is very good, just one non-match, fixed with this
```
UPDATE temp.provincial 
SET electoral_district = 'Prince George-Mackenzie' 
WHERE electoral_district = 'Prince George-MacKenzie';`
 
-- check results
SELECT 
 s.bc_electoral_district_id,
 s.electoral_district_name,
 r.electoral_district,
 r.mla_name,
 r.mla_party
FROM whse_admin_boundaries.ped_prov_electoral_dist_poly s
FULL OUTER JOIN
temp.provincial r
ON s.electoral_district_name = r.electoral_district
```

Federal data requires a few more fixes.

```
UPDATE mit.federal_electoral_boundary 
SET enname = REPLACE(enname, '--', ' - ')
WHERE enname LIKE '%--%';

UPDATE mit.federal_electoral_boundary 
SET enname = 'West Vancouver - Sunshine Coast - Sea to Sky Country'
WHERE enname = 'West Vancouver¿Sunshine Coast¿Sea to Sky Country';

UPDATE temp.federal
SET riding_name = 'Pitt Meadows - Maple Ridge - Mission'
WHERE riding_name = 'Pitt Meadows- Maple Ridge - Mission';

UPDATE temp.federal
SET riding_name = 'Esquimalt - Juan de Fuca'
WHERE riding_name = 'Esquimalt/Juan de Fuca';

UPDATE temp.federal
SET riding_name = 'Skeena - Bulkley Valley'
WHERE riding_name = 'Skeena -Bulkley Valley';

-- check 
SELECT 
 s.fednum,
 s.enname,
 r.riding_name,
 r.mp_name,
 r.mp_party
FROM mit.federal_electoral_boundary s
FULL OUTER JOIN
temp.federal r
ON s.enname = r.riding_name
```


### Generate lookup, linking communities to ridings
```
-- generate provincial electoral area lookup
SELECT * FROM 
(SELECT
 c.census_subdivision_id,
 c.clab_id,
 c.community_name,
 p.bc_electoral_district_id AS prov_electoral_district_id,
 p.electoral_district_name AS prov_electoral_district_name,
 SUM(st_area(c.geom)) / 10000 AS community_ha,
 SUM(st_area(st_intersection(c.geom, p.geom))) / 10000 AS overlap_ha,
 SUM(st_area(st_intersection(c.geom, p.geom))) / SUM(st_area(c.geom)) AS overlap_pct
FROM mit.communities c
INNER JOIN
whse_admin_boundaries.ped_prov_electoral_dist_poly p
ON st_intersects(c.geom, p.geom)
GROUP BY 
 c.census_subdivision_id,
 c.clab_id,
 c.community_name,
 p.bc_electoral_district_id, 
 p.electoral_district_name
ORDER BY community_name) AS foo
where overlap_ha > 1;

-- generate federal electoral area lookup
SELECT * FROM 
(SELECT
 c.census_subdivision_id,
 c.clab_id,
 c.community_name,
 p.fednum AS federal_electoral_area_number,
 p.enname AS federal_electoral_area_name,
 SUM(st_area(c.geom)) / 10000 AS community_ha,
 SUM(st_area(st_intersection(c.geom, p.geom))) / 10000 AS overlap_ha,
 SUM(st_area(st_intersection(c.geom, p.geom))) / SUM(st_area(c.geom)) AS overlap_pct
FROM mit.communities c
INNER JOIN mit.federal_electoral_boundary p
ON st_intersects(c.geom, p.geom)
GROUP BY 
 c.census_subdivision_id,
 c.clab_id,
 c.community_name,
 p.fednum,
 p.enname
ORDER BY community_name) AS foo
where overlap_ha > 1;
```

These resulting tables have to be manually QA'ed to remove bad links (boundaries from source datasets are mapped at different scales)

### Link municipal gov to CSD
```
-- preliminary join
SELECT 
 csd.census_subdivision_id,
 csd.census_subdivision_name,
 m.community,
 m.top_elected_official,
 m.n_elected_official
FROM 
(SELECT * FROM mit.cen_census_subdivisions
 WHERE census_subdivision_type_code IN ('CY', 'DM', 'RGM', 'T', 'VL', 'IM')) csd
FULL OUTER JOIN temp.municipal m
ON csd.census_subdivision_name =  m.community
```

A few non-matches have to be fixed manually (Langley and North Vancouver are not unique). FN local govt dropped from this table, Jumbo Glacier added.
Several local govts not included in source file:
```
Canal Flats
Queen Charlotte
Radium Hot Springs
Sun Peaks Mountain
Jumbo Glacier
```

