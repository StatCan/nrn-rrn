-- Drop / create sequences for incremental integer columns.
DROP SEQUENCE IF EXISTS ferryseg_seq;
CREATE TEMP SEQUENCE ferryseg_seq;

-- Create temporary tables (subqueries to be reused).

-- Create temporary table(s): route name.
WITH route_name_link AS
  (SELECT segment_id,
          route_name_en,
          route_name_fr,
          ROW_NUMBER() OVER (PARTITION BY segment_id)
   FROM public.route_name_link route_name_link_partition
   LEFT JOIN public.route_name route_name ON route_name_link_partition.route_name_id = route_name.route_name_id),
route_name_1 AS
  (SELECT *
   FROM route_name_link
   WHERE row_number = 1),
route_name_2 AS
  (SELECT *
   FROM route_name_link
   WHERE row_number = 2),
route_name_3 AS
  (SELECT *
   FROM route_name_link
   WHERE row_number = 3),
route_name_4 AS
  (SELECT *
   FROM route_name_link
   WHERE row_number = 4),

-- Create temporary table(s): route number.
route_number_link AS
  (SELECT segment_id,
          route_number,
          ROW_NUMBER() OVER (PARTITION BY segment_id)
   FROM public.route_number_link route_number_link_partition
   LEFT JOIN public.route_number route_number ON route_number_link_partition.route_number_id = route_number.route_number_id),
route_number_1 AS
  (SELECT *
   FROM route_number_link
   WHERE row_number = 1),
route_number_2 AS
  (SELECT *
   FROM route_number_link
   WHERE row_number = 2),
route_number_3 AS
  (SELECT *
   FROM route_number_link
   WHERE row_number = 3),
route_number_4 AS
  (SELECT *
   FROM route_number_link
   WHERE row_number = 4),
route_number_5 AS
  (SELECT *
   FROM route_number_link
   WHERE row_number = 5),

-- Create primary table.

-- Compile all NRN attributes into a single table.
SELECT REPLACE(ferry_source.ferry_id::text, '-', '') AS nid,
       acquisition_technique_lookup.value_en AS acqtech,
       ferry_source.planimetric_accuracy AS accuracy,
       provider_lookup.value_en AS provider,
       ferry_source.creation_date AS credate,
       ferry_source.revision_date AS revdate,
       closing_period_lookup.value_en AS closing,
       functional_road_class_lookup.value_en AS roadclass,
       ferry_source.geometry,
       route_name_1.route_name_en AS rtename1en,
       route_name_1.route_name_fr AS rtename1fr,
       route_name_2.route_name_en AS rtename2en,
       route_name_2.route_name_fr AS rtename2fr,
       route_name_3.route_name_en AS rtename3en,
       route_name_3.route_name_fr AS rtename3fr,
       route_name_4.route_name_en AS rtename4en,
       route_name_4.route_name_fr AS rtename4fr,
       route_number_1.route_number AS rtnumber1,
       route_number_2.route_number AS rtnumber2,
       route_number_3.route_number AS rtnumber3,
       route_number_4.route_number AS rtnumber4,
       route_number_5.route_number AS rtnumber5,
       nextval('ferryseg_seq') AS ferrysegid,
       {{ source_code }} AS datasetnam,
       {{ metacover }} AS metacover,
       {{ specvers }} AS specvers
FROM

  -- Subset records to the source province / territory.
 (SELECT ferry.*
  FROM public.ferry ferry
  WHERE ferry.province = {{ source_code }}) ferry_source

-- Join with all linked datasets.
LEFT JOIN route_name_1 ON ferry_source.ferry_id = route_name_1.segment_id
LEFT JOIN route_name_2 ON ferry_source.ferry_id = route_name_2.segment_id
LEFT JOIN route_name_3 ON ferry_source.ferry_id = route_name_3.segment_id
LEFT JOIN route_name_4 ON ferry_source.ferry_id = route_name_4.segment_id
LEFT JOIN route_number_1 ON ferry_source.ferry_id = route_number_1.segment_id
LEFT JOIN route_number_2 ON ferry_source.ferry_id = route_number_2.segment_id
LEFT JOIN route_number_3 ON ferry_source.ferry_id = route_number_3.segment_id
LEFT JOIN route_number_4 ON ferry_source.ferry_id = route_number_4.segment_id
LEFT JOIN route_number_5 ON ferry_source.ferry_id = route_number_5.segment_id

-- Join with lookup tables.
LEFT JOIN public.acquisition_technique_lookup acquisition_technique_lookup ON ferry_source.acquisition_technique = acquisition_technique_lookup.code
LEFT JOIN public.provider_lookup provider_lookup ON ferry_source.provider = provider_lookup.code
LEFT JOIN public.closing_period_lookup closing_period_lookup ON ferry_source.closing_period = closing_period_lookup.code
LEFT JOIN public.functional_road_class_lookup functional_road_class_lookup ON ferry_source.functional_road_class = functional_road_class_lookup.code