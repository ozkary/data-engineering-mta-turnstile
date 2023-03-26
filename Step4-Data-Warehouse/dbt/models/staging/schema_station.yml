version: 2

sources:
    - name: staging
      #For bigquery:
      database: ozkary-de-101

      # For postgres:
      # database: production

      schema: mta_data

      # loaded_at_field: record_loaded_at
      tables:
        - name: remote_booth_station
         # freshness:
           # error_after: {count: 6, period: hour}

models:
    - name: stg_station
      description: >
        Subway station names
      columns:
          - name: station_id
            description: The station identifier
            tests:
                - unique:
                    severity: warn
                - not_null:
                    severity: warn
          - name: station_name
            description: the station name
          