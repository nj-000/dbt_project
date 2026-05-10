
    
    

select
    vendor_id as unique_field,
    count(*) as n_records

from "taxi_rides_ny"."dev"."dim_vendors"
where vendor_id is not null
group by vendor_id
having count(*) > 1


