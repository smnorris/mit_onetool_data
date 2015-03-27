-- create a community table (points)
DROP TABLE if EXISTS mit.communities_pt;

CREATE TABLE mit.communities_pt
(community_id SERIAL,
 census_subdivision_id integer,
 clab_id text,
 community_name TEXT,
 community_type TEXT,
 lat float,
 long float,
 geom geometry);

-- insert incorporated CSDs
INSERT INTO mit.communities_pt (census_subdivision_id, community_name, community_type, lat, long, geom)
SELECT
  csd.census_subdivision_id::INT,
  csd.census_subdivision_name,
  'MUNI',
  r.reppoint_latitude,
  r.reppoint_longitude,
  st_transform(st_setsrid(st_makepoint(r.reppoint_longitude, r.reppoint_latitude),4326), 3005) AS geom
FROM mit.cen_census_subdivisions csd
INNER JOIN mit.cen_census_subdivision_refpts r
ON csd.census_subdivision_id = r.csd_uid
WHERE csd.census_subdivision_type_code IN ('CY', 'DM', 'RGM', 'T', 'VL', 'IM');

-- insert FN CSDs
INSERT INTO mit.communities_pt (census_subdivision_id, community_name, community_type, lat, long, geom)
SELECT fn.census_subdivision_id::INT,
  fn.fn_name_1,
  'FN',
  r.reppoint_latitude,
  r.reppoint_longitude,
  st_transform(st_setsrid(st_makepoint(r.reppoint_longitude, r.reppoint_latitude),4326), 3005) AS geom
FROM mit.econ_whse_first_nations_population_bc fn
INNER JOIN mit.cen_census_subdivision_refpts r
ON fn.census_subdivision_id = r.csd_uid::INT;

-- insert FNs with no CSD from IR table
INSERT INTO mit.communities_pt (clab_id, community_name, community_type, lat, long, geom)
SELECT fn.clab_id, fn.fn_name_1, 'FN',
st_y(st_transform(st_centroid(ir.geom), 4326)) AS lat,
st_x(st_transform(st_centroid(ir.geom), 4326)) AS long,
st_centroid(ir.geom) AS geom
FROM mit.econ_whse_first_nations_population_bc fn
INNER JOIN whse_admin_boundaries.adm_indian_reserves_bands_sp ir
ON fn.clab_id::TEXT = ir.clab_id
WHERE fn.clab_id IS NOT NULL;

-- insert JUMBO from tantalis
INSERT INTO mit.communities_pt (community_name, community_type, lat, long, geom)
SELECT 'Jumbo Glacier', 'MUNI',
st_y(st_transform(st_centroid(geom), 4326)) AS lat,
st_x(st_transform(st_centroid(geom), 4326)) AS long,
st_centroid(geom) AS geom
FROM whse_tantalis.ta_municipalities_svw
WHERE municipality_name LIKE 'JUMBO%';