SELECT DISTINCT
    trk.*,
    st.station_stnenname,
    st.station_stntype,
    st.station_stnusr1ena
FROM

(SELECT DISTINCT
  -- census year isn't in the source file
  2011 AS census_year,
  csd.census_subdivision_id,
  track.usetype AS track_usetype,
  track.operatoena AS track_operatoena,
  track.ownerena AS track_ownerena
FROM mit.cen_census_subdivisions csd
INNER JOIN whse_basemapping.nrn_track track
ON ST_Intersects(csd.geom, track.geom)) AS trk

FULL OUTER JOIN

(SELECT DISTINCT
  2011 AS census_year,
  csd.census_subdivision_id,
  stn.stnenname AS station_stnenname,
  stn.stntype AS station_stntype,
  stn.stnusr1ena AS station_stnusr1ena
FROM mit.cen_census_subdivisions csd
INNER JOIN whse_basemapping.nrn_station stn
ON ST_Intersects(csd.geom, stn.geom)) AS st

ON trk.census_subdivision_id = st.census_subdivision_id