

  create or replace view `serious-music-469407-f1`.`banking_silver`.`stg_ecom_products`
  OPTIONS()
  as with 

source as (

    select * from `serious-music-469407-f1`.`banking_bronze`.`ecom_products`

),

renamed as (

    select
        price,
        UPPER(category) AS category,
        UPPER(product_name) AS product_name,
        product_id

    from source

)

select * from renamed;

