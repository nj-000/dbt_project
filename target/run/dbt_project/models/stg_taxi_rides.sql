
  
  create view "taxi_rides_ny"."dev"."stg_taxi_rides__dbt_tmp" as (
    -- This tells dbt to create a view in MotherDuck


WITH trip_data AS (
    SELECT * FROM "taxi_rides_ny"."prod"."yellow_tripdata"
)

SELECT
    -- Convert identifiers
    CAST(VendorID AS INT) AS vendor_id,
    CAST(PULocationID AS INT) AS pickup_location_id,
    CAST(DOLocationID AS INT) AS dropoff_location_id,

    -- Timestamps
    tpep_pickup_datetime AS pickup_datetime,
    tpep_dropoff_datetime AS dropoff_datetime,

    -- Metrics
    trip_distance,
    fare_amount,
    tip_amount,
    total_amount

FROM trip_data
WHERE trip_distance > 0 AND total_amount > 0
  );
