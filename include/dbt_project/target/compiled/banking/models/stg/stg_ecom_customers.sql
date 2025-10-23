with 

source as (

    select * from `serious-music-469407-f1`.`banking_bronze`.`ecom_customers`

),

renamed as (

    select
        DATE(TIMESTAMP_MILLIS(signup_date)) as signup_date,
        UPPER(last_name) AS last_name,
        email,
        UPPER(first_name) AS first_name,
        customer_id

    from source

)

select * from renamed