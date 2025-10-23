
    ALTER TABLE serious-music-469407-f1.banking_silver.int_ecom_orders_enriched
    SET OPTIONS (require_partition_filter = true);

    ALTER TABLE serious-music-469407-f1.banking_gold.mart_ecom_sales_summary
    SET OPTIONS (require_partition_filter = true);
