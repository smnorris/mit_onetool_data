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