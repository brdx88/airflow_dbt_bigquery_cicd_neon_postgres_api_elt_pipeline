with 

source as (

    select * from {{ source('banking_bronze', 'ecom_orders') }}

),

renamed as (

    select
        product_id,
        customer_id,
        total_amount,
        quantity,
        order_date,
        id

    from source

)

select * from renamed