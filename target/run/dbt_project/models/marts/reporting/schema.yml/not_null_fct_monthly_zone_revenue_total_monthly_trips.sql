
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select total_monthly_trips
from "taxi_rides_ny"."dev"."fct_monthly_zone_revenue"
where total_monthly_trips is null



  
  
      
    ) dbt_internal_test