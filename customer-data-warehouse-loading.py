# Import necessary libraries for Databricks
from pyspark.sql import SparkSession
from pyspark.sql.functions import concat_ws

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Customer Load ETL") \
    .getOrCreate()

# Define source and target configurations
# Assuming Oracle JDBC connection details are available as Databricks secrets or environment variables
oracle_source_url = "jdbc:oracle:thin:@<Oracle_Source_Host>:<Port>:<Service_Name>"
oracle_target_url = "jdbc:oracle:thin:@<Oracle_Target_Host>:<Port>:<Service_Name>"

# Define source and target table names
source_table = "CUSTOMER_SRC"
target_table = "CUSTOMER_DW"

# Load source data from Oracle
customer_src_df = spark.read.format("jdbc") \
    .option("url", oracle_source_url) \
    .option("dbtable", source_table) \
    .option("user", "<username>") \
    .option("password", "<password>") \
    .load()

# Transformation: Concatenate FIRST_NAME and LAST_NAME to create FULL_NAME
# Assuming FIRST_NAME and LAST_NAME are columns in the CUSTOMER_SRC table
customer_transformed_df = customer_src_df.withColumn(
    "FULL_NAME", concat_ws(" ", customer_src_df.FIRST_NAME, customer_src_df.LAST_NAME)
)

# Write transformed data to target Oracle database
customer_transformed_df.write.format("jdbc") \
    .option("url", oracle_target_url) \
    .option("dbtable", target_table) \
    .option("user", "<username>") \
    .option("password", "<password>") \
    .mode("overwrite") \
    .save()

# Error handling and logging
# In a production scenario, consider using Databricks' logging mechanisms or external monitoring tools
try:
    # ETL process code here
    pass
except Exception as e:
    # Log the error
    print(f"Error occurred: {e}")
    # Optionally, write error details to a log file or monitoring system

# Comments:
# - The transformation logic from Informatica's Expression transformation is replicated using Spark's concat_ws function.
# - Connection details are assumed to be managed securely via Databricks secrets or environment variables.
# - Error handling is basic; consider integrating with Databricks' logging or external monitoring for robust solutions.
# - This script assumes the presence of FIRST_NAME and LAST_NAME columns in the source table.

# Stop the Spark session
spark.stop()
```