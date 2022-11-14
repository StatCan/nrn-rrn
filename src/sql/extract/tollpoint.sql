-- Create temporary table(s): place name.
place_name AS
  (SELECT *
   FROM public.basic_block basic_block
   LEFT JOIN public.census_block ON basic_block.cb_uid = public.census_block.cb_uid
   LEFT JOIN public.census_subdivision ON basic_block.csd_uid = public.census_subdivision.csd_uid)

-- Compile all NRN attributes into a single table.
SELECT REPLACE(toll_point.toll_point_id::text, '-', '') AS nid,
       REPLACE(toll_point.segment_id::text, '-', '') AS roadnid,
       toll_point_type_lookup.value_en AS tollpttype,
       acquisition_technique_lookup.value_en AS acqtech,
       toll_point.planimetric_accuracy AS accuracy,
       provider_lookup.value_en AS provider,
       toll_point.creation_date AS credate,
       toll_point.revision_date AS revdate,
       toll_point.geometry,
       {{ source_code }} AS datasetnam,
       {{ metacover }} AS metacover,
       {{ specvers }} AS specvers
FROM

  -- Subset records to the source province / territory.
  (SELECT segment_source.segment_id
   FROM
     (SELECT segment.segment_id,
             place_name_l.province AS province_l,
             place_name_r.province AS province_r
      FROM public.segment segment
      LEFT JOIN place_name place_name_l ON segment.bb_uid_l = place_name_l.bb_uid
      LEFT JOIN place_name place_name_r ON segment.bb_uid_r = place_name_r.bb_uid) segment_source
   WHERE segment_source.province_l = {{ source_code }} OR segment_source.province_r = {{ source_code }}) nrn

INNER JOIN public.toll_point toll_point ON nrn.segment_id = toll_point.segment_id

-- Join with lookup tables.
LEFT JOIN public.acquisition_technique_lookup acquisition_technique_lookup ON toll_point.acquisition_technique = acquisition_technique_lookup.code
LEFT JOIN public.provider_lookup provider_lookup ON toll_point.provider = provider_lookup.code
LEFT JOIN public.toll_point_type_lookup toll_point_type_lookup ON toll_point.toll_point_type = toll_point_type_lookup.code