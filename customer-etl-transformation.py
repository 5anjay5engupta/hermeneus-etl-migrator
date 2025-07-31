# Import necessary libraries for Databricks
from pyspark.sql import SparkSession
from pyspark.sql.functions import concat_ws

# Initialize Spark session
spark = SparkSession.builder.appName("Customer_ETL_Transform").getOrCreate()

# Step 1: Read CSV Input
# Assumption: The CSV file is accessible from Databricks File System (DBFS)
# and the path is adjusted accordingly.
csv_file_path = "/dbfs/data/source/customer.csv"

# Read the CSV file into a DataFrame
customer_df = spark.read.csv(csv_file_path, header=True, inferSchema=True)

# Step 2: Data Transformation - Calculator
# Combine first_name and last_name into full_name
# Using concat_ws to handle potential nulls and ensure proper spacing
customer_df = customer_df.withColumn("full_name", concat_ws(" ", customer_df.first_name, customer_df.last_name))

# Step 3: MySQL Output
# Assumption: MySQL connection details are configured in Databricks secrets or environment variables
mysql_url = "jdbc:mysql://<mysql-server>:3306/<database>"
mysql_properties = {
    "user": "<username>",
    "password": "<password>",
    "driver": "com.mysql.jdbc.Driver"
}

# Write the transformed data to MySQL
customer_df.write.jdbc(url=mysql_url, table="customer_dw", mode="overwrite", properties=mysql_properties)

# Error Handling and Logging
# In a production environment, consider using try-except blocks and logging libraries
# such as log4j for better error handling and logging.

# Comments:
# - The CSV input path is assumed to be accessible from DBFS.
# - MySQL connection details should be securely managed using Databricks secrets.
# - The transformation logic is preserved by using Spark SQL functions.
# - The write operation uses JDBC, a common practice in Databricks for database interactions.

# 
# Assumptions regarding file paths and database connections are based on common configurations in Databricks.
# Potential limitations include the handling of nulls in name concatenation and the need for secure management of credentials.