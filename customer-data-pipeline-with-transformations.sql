-- dbt Model: customer_transformed.sql
-- This model processes customer data by transforming it according to business rules.
-- Assumptions: The source data is available in a table or view named `customer_source`.

{{ config(
    materialized='table',
    description='Transforms customer data by adding full_name, processed_date, and customer_key.'
) }}

with customer_source as (

    -- Source data extraction
    select
        customer_id,
        first_name,
        last_name,
        email
    from {{ source('source_schema', 'customer_source') }}

),

customer_transformed as (

    -- Transformation logic
    select
        customer_id,
        first_name,
        last_name,
        email,
        {{ dbt_utils.concat([first_name, last_name], ' ') }} as full_name,  -- Concatenating first and last names
        current_date() as processed_date,  -- Adding the current date
        md5(cast(customer_id as text)) as customer_key  -- Hashing customer_id for a unique key
    from customer_source

)

-- Final selection for the transformed model
select * from customer_transformed;

-- Note: Ensure that the `source_schema` and `customer_source` are correctly configured in dbt sources.

-- dbt Documentation and Configuration
-- This model is part of the customer data processing pipeline.
-- It assumes that the source data is clean and correctly formatted.
-- Error handling and logging should be managed by dbt's built-in mechanisms and the underlying database.

```