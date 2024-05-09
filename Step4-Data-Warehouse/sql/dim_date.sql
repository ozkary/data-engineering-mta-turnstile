CREATE TABLE dim_date (
  date_id INT NOT NULL PRIMARY KEY,  -- Surrogate key for the date dimension
  full_date DATE NOT NULL,          -- Full date in YYYY-MM-DD format
  year INT NOT NULL,                -- Year (e.g., 2024)
  quarter INT NOT NULL,             -- Quarter of the year (1-4)
  month INT NOT NULL,               -- Month of the year (1-12)
  month_name VARCHAR(20) NOT NULL,    -- Name of the month (e.g., January)
  day INT NOT NULL,                 -- Day of the month (1-31)
  day_of_week INT NOT NULL,            -- Day of the week (1-7, where 1=Sunday)
  day_of_week_name VARCHAR(20) NOT NULL, -- Name of the day of the week (e.g., Sunday)
  is_weekend BOOLEAN NOT NULL,        -- Flag indicating weekend (TRUE) or weekday (FALSE)
  is_holiday BOOLEAN NOT NULL,        -- Flag indicating holiday (TRUE) or not (FALSE)
  fiscal_year INT,                   -- Fiscal year (optional)
  fiscal_quarter INT                 -- Fiscal quarter (optional)  -- Optional
);