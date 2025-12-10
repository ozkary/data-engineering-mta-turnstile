CREATE OR REPLACE VIEW `ozkary-de-101`.`mta_data`.`vw_ext_turnstile` AS
SELECT
  -- Excluding int64_field_0 (the unwanted column)

  t.CA ,
  t.UNIT ,
  t.SCP ,
  t.STATION,
  t.LINENAME,
  t.DIVISION,
  t.DATE,
  t.TIME,
  t.DESC,
  t.ENTRIES,
  t.EXITS

FROM
  `mta_data.ext_turnstile` AS t
;