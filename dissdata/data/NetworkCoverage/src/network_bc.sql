-- overlay CSD and network coverage in GIS package to produce csd_network
-- upload result to database and run this query to report on csd coverage levels

DROP TABLE IF EXISTS mitdataprep.telecommunications_csd;

CREATE TABLE mitdataprep.telecommunications_csd AS
SELECT
  overlap.census_subdivision_id::int4,
  round(sum(overlap.broadband_coverage *
      (overlap.area_overlap / ST_Area(c.geom)))::numeric, 3) as broadband_coverage,
  round(sum(overlap.dsl_cable_coverage * (overlap.area_overlap / ST_Area(c.geom)))::numeric, 3) as dsl_cable_coverage,
  round(sum(overlap.fixed_wireless_coverage * (overlap.area_overlap / ST_Area(c.geom)))::numeric, 3) as fixed_wireless_coverage,
  round(sum(overlap.mobility_coverage * (overlap.area_overlap / ST_Area(c.geom)))::numeric, 3) as mobility_coverage,
  round(sum(overlap.satellite_coverage * (overlap.area_overlap / ST_Area(c.geom)))::numeric, 3) as satellite_coverage
  --overlap.area_overlap / ST_Area(n.geom) as area_overlap
FROM
(SELECT
   hex_code_id,
   census_subdivision_id,
   broadband_coverage,
   dsl_cable_coverage,
   fixed_wireless_coverage,
   mobility_coverage,
   satellite_coverage,
   SUM(ST_Area(geom)) as area_overlap
FROM mitdataprep.network_csd
WHERE hex_code_id <> ''
AND hex_code_id is not NULL
and census_subdivision_id <> ''
and census_subdivision_id is not NULL
GROUP BY
  hex_code_id,
  census_subdivision_id,
  broadband_coverage,
  dsl_cable_coverage,
  fixed_wireless_coverage,
  mobility_coverage,
  satellite_coverage) as overlap
INNER JOIN mitdataprep.cen_census_subdivisions c
ON overlap.census_subdivision_id = c.census_subdivision_id
GROUP BY overlap.census_subdivision_id
ORDER BY census_subdivision_id;

CREATE INDEX ON mitdataprep.telecommunications_csd(census_subdivision_id);

DROP TABLE IF EXISTS mitdataprep.telecommunications_csd_sp;

CREATE TABLE mitdataprep.telecommunications_csd_sp AS
SELECT
  tele.*,
  csd.geom
FROM mitdataprep.telecommunications_csd tele
INNER JOIN mitdataprep.cen_census_subdivisions csd
ON tele.census_subdivision_id = csd.census_subdivision_id::int4;