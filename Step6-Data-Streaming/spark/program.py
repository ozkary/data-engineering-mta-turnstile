import argparse
from ast import List
from pathlib import Path
import os
import pyspark
from pyspark.sql import SparkSession, DataFrame, types
import pyspark.sql.functions as F
from consumer import SparkSettings, SparkConsumer
from schema import turnstiles_schema

PROJECT = 'ozkary-de-101'
BUCKET = 'gs://ozkary_data_lake_ozkary-de-101/turnstile'

def write_to_console(df: DataFrame, output_mode: str = 'append', processing_time: str = '5 seconds') -> None:
    """
        Output stream values to the console
    """
    console_query = df.writeStream\
        .outputMode(output_mode) \
        .trigger(processingTime=processing_time) \
        .format("console") \
        .option("truncate", False) \
        .start()
    
    console_query.awaitTermination()     

def main_flow(params) -> None:
    """
    main flow to process stream messages with spark
    """    
    topic = params.topic
    group_id = params.group    
    client_id = params.client
    config_path = params.config    
    spark_master = params.master

    # create the consumer settings
    spark_settings = SparkSettings(config_path, topic, group_id, client_id)    
        
    # create the spark consumer
    spark_session = SparkSession.builder \
            .appName("turnstiles-consumer") \
            .getOrCreate()                
    
    spark_session.sparkContext.setLogLevel("INFO")
    
    # create an instance of the consumer class
    consumer = SparkConsumer(spark_settings, topic, group_id, client_id)

    # set the data frame stream
    consumer.read_kafka_stream(spark_session) 

    # parse the messages
    df_messages = consumer.parse_messages(schema=turnstiles_schema)
    write_to_console(df_messages)
    
    # define a window for 5 minutes aggregations group by station
    window_duration = '5 minutes'
    window_slide = '5 minutes'

    df_windowed = consumer.agg_messages(window_duration, window_slide)
        
    write_to_console(df_windowed)

    # Write the aggregated data to a blob storage as compressed CSV files
    # query = df_windowed.writeStream\
    #     .outputMode("update")\
    #     .foreachBatch(lambda batch_df, batch_id: batch_df.write\
    #         .mode("overwrite")\
    #         .csv(BUCKET)  # Replace with your blob storage path
    #     )\
    #     .start()
           
    spark_session.streams.awaitAnyTermination()


if __name__ == "__main__":
    """
        Main entry point for streaming data between kafka and spark        
    """
    os.system('clear')
    print('Spark streaming running...')
    parser = argparse.ArgumentParser(description='Producer : --topic mta-turnstile --group spark_group --client app1 --config path-to-config')
    
    parser.add_argument('--topic', required=True, help='kafka topics')    
    parser.add_argument('--group', required=True, help='consumer group')
    parser.add_argument('--client', required=True, help='client id group')
    parser.add_argument('--config', required=True, help='cloud settings')    
    parser.add_argument('--master', required=False, help='Spark master')        
    args = parser.parse_args()

    if (args.master is None):
        args.master = 'spark://localhost:7077'

    main_flow(args)

    print('end')

# Usage
# load spark shell
# spark-shell --packages org.apache.spark:spark-sql-kafka-0-10_2.12:your_spark_version

# run the app
# python3 program.py --topic mta-turnstile --group turnstile --client appTurnstile --config ~/.kafka/azure.properties
# spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2 program.py --topic mta-turnstile --group turnstile --client appTurnstile --config ~/.kafka/azure.properties

# export KAFKA_OPTS="java.security.auth.login.config=~/.kafka/azure.properties.jaas"

# spark-submit --conf spark.kafka.sasl.jaas.config=~/.kafka/azure.properties.jaas --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2 program.py --topic mta-turnstile --group turnstile --client appTurnstile --config ~/.kafka/azure.properties

# spark-shell --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2