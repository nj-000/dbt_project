





with validation_errors as (

    select
        pickup_zone, revenue_month, service_type
    from "taxi_rides_ny"."dev"."fct_monthly_zone_revenue"
    group by pickup_zone, revenue_month, service_type
    having count(*) > 1

)

select *
from validation_errors


