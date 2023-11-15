from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType

# Define the schema for the incoming data
turnstiles_schema = StructType([
    StructField("A/C", StringType()),
    StructField("UNIT", StringType()),
    StructField("SCP", StringType()),
    StructField("STATION", StringType()),
    StructField("LINENAME", StringType()),
    StructField("DIVISION", StringType()),
    StructField("DATE", StringType()),
    StructField("TIME", StringType()),
    StructField("DESC", StringType()),
    StructField("ENTRIES", IntegerType()),
    StructField("EXITS", IntegerType()),
    StructField("ID", StringType()),
    StructField("TIMESTAMP", StringType())
])