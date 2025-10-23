
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select customer_id
from `serious-music-469407-f1`.`banking_silver`.`int_ecom_orders_enriched`
where customer_id is null



  
  
      
    ) dbt_internal_test