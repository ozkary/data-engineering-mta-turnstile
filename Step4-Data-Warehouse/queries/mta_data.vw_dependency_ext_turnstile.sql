CREATE OR REPLACE VIEW `ozkary-de-101`.`mta_data`.`vw_dependency_ext_turnstile` AS
SELECT
  t.table_name AS dependent_view_name,
  t.view_definition
FROM
  -- Query the INFORMATION_SCHEMA.VIEWS for the specific dataset
  `ozkary-de-101`.`mta_data`.INFORMATION_SCHEMA.VIEWS AS t
WHERE
  -- Search the view definition text for the name of the external table.
  -- This reliably finds all views that directly reference the source table.
  LOWER(t.view_definition) LIKE '%ext_turnstile%'
  -- Exclude the current view itself from the results
  AND t.table_name != 'vw_dependency_ext_turnstile'
;