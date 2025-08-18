-- models/customer_load.sql

{{ config(
    materialized='incremental',
    unique_key='customer_id',
    description='Transforms and loads customer data from source to target data warehouse'
) }}

with source_data as (

    -- Source extraction
    select
        customer_id,
        first_name,
        last_name
    from {{ source('oracle_source', 'customer_src') }}

),

transformed_data as (

    -- Transformation logic
    select
        customer_id,
        first_name || ' ' || last_name as full_name
    from source_data

)

-- Load into target
select
    customer_id,
    full_name
from transformed_data

```

```yaml
# models/schema.yml

version: 2

models:
  - name: customer_load
    description: "Transforms and loads customer data from source to target data warehouse"
    columns:
      - name: customer_id
        description: "Unique identifier for each customer"
      - name: full_name
        description: "Concatenated full name of the customer"

sources:
  - name: oracle_source
    tables:
      - name: customer_src
        description: "Source table containing raw customer data"

```

### Assumptions and Explanations:
1. **Data Transformation Logic**: The transformation logic from the Informatica Expression transformation is preserved using SQL string concatenation.
2. **Data Lineage and Sequence**: The sequence of operations is maintained using CTEs to clearly separate extraction and transformation steps.
3. **Connection Adaptation**: The source is configured using dbt's `source` function, assuming a source configuration exists in `dbt_project.yml`.
4. **Error Handling and Logging**: dbt inherently manages logging and error handling during model execution.
5. **Best Practices**: The model is configured to be incremental, assuming that the `customer_id` is a unique key for incremental loads.
6. **Comments and Documentation**: Inline comments and a separate YAML file provide documentation and context for the model.