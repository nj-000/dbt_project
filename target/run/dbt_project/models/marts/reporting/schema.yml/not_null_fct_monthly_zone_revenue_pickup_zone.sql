
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select pickup_zone
from "taxi_rides_ny"."dev"."fct_monthly_zone_revenue"
where pickup_zone is null



  
  
      
    ) dbt_internal_test