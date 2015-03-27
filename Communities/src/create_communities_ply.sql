-- create a community table
DROP TABLE if EXISTS mit.communities_ply;

CREATE TABLE mit.communities_ply
(community_id SERIAL,
 census_subdivision_id integer,
 clab_id text,
 community_name TEXT,
 community_type TEXT,
 geom geometry);

-- insert incorporated CSDs
INSERT INTO mit.communities_ply (census_subdivision_id, community_name, community_type, geom)
SELECT census_subdivision_id::INT, census_subdivision_name, 'MUNI', geom
FROM mit.cen_census_subdivisions
WHERE census_subdivision_type_code IN ('CY', 'DM', 'RGM', 'T', 'VL', 'IM');

-- insert FN CSDs
INSERT INTO mit.communities_ply (census_subdivision_id, community_name, community_type, geom)
SELECT fn.census_subdivision_id::INT, fn.fn_name_1, 'FN', csd.geom
FROM mit.econ_whse_first_nations_population_bc fn
INNER JOIN mit.cen_census_subdivisions csd
ON fn.census_subdivision_id = csd.census_subdivision_id::INT;

-- insert FNs with no CSD from IR table
INSERT INTO mit.communities_ply (clab_id, community_name, community_type, geom)
SELECT fn.clab_id, fn.fn_name_1, 'FN', ir.geom
FROM mit.econ_whse_first_nations_population_bc fn
INNER JOIN whse_admin_boundaries.adm_indian_reserves_bands_sp ir
ON fn.clab_id::TEXT = ir.clab_id
WHERE fn.clab_id IS NOT NULL;

-- insert JUMBO from tantalis
INSERT INTO mit.communities_ply (community_name, community_type, geom)
SELECT 'Jumbo Glacier', 'MUNI', geom
FROM whse_tantalis.ta_municipalities_svw
WHERE municipality_name LIKE 'JUMBO%';