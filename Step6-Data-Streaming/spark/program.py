#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  2023 ozkary.com.
#
#  MTA turnstile data engineering and analysis
#

# Standard Library Imports
import argparse
from ast import List
from pathlib import Path
import os

# Third-Party Library Imports
from pyspark.sql import SparkSession, DataFrame, types
import pyspark.sql.functions as F
from consumer import SparkSettings, SparkConsumer
from schema import turnstiles_schema
from prefect import flow

# Local Module Imports
PROJECT = 'ozkary-de-101'
BUCKET = 'gs://ozkary_data_lake_ozkary-de-101/turnstile'


def write_to_console(df: DataFrame, output_mode: str = 'append', processing_time: str = '15 seconds') -> None:
    """
        Output stream values to the console
    """
    console_query = df.writeStream\
        .outputMode(output_mode) \
        .trigger(processingTime=processing_time) \
        .format("console") \
        .option("truncate", False) \
        .start()
    
    # this suspends execution until the stream is stopped
    # console_query.awaitTermination()     


# write a streaming data frame to storage ./storage
def write_to_storage(df: DataFrame, output_mode: str = 'append', processing_time: str = '15 seconds') -> None:
    """
        Output stream values to the console
    """    
    # df_csv = df.select(
    #     "A/C", "UNIT", "SCP", "STATION", "LINENAME", "DIVISION", "DATE", "DESC",
    #     "ENTRIES", "EXITS"
    # )
    #    
    print("Storage: DataFrame Schema:")
    df.printSchema()
        
    # .partitionBy("STATION") \
    storage_query = df.writeStream \
        .outputMode(output_mode) \
        .trigger(processingTime=processing_time) \
        .format("csv") \
        .option("header", True) \
        .option("path", "./storage") \
        .option("checkpointLocation", "./checkpoint") \
        .option("truncate", False) \
        .start()
    
    # storage_query.awaitTermination()
@flow (name="MTA Spark Data Stream flow", description="Data Streaming Flow")
def main_flow(params) -> None:
    """
    main flow to process stream messages with spark
    """    
    topic = params.topic
    group_id = params.group    
    client_id = params.client
    config_path = params.config    

    # define a window for n minutes aggregations group by station
    default_span = '5 minutes'
    window_duration = default_span if params.duration is None else f'{params.duration} minutes'
    window_slide = default_span if params.slide is None else f'{params.slide} minutes'
    
    # create the consumer settings
    spark_settings = SparkSettings(config_path, topic, group_id, client_id)    
        
    # create the spark consumer
    spark_session = SparkSession.builder \
            .appName("turnstiles-consumer") \
            .getOrCreate()                
    
    spark_session.sparkContext.setLogLevel("WARN")
    
    # create an instance of the consumer class
    consumer = SparkConsumer(spark_settings, topic, group_id, client_id)

    # set the data frame stream
    consumer.read_kafka_stream(spark_session) 
    
    # parse the messages
    df_messages = consumer.parse_messages(schema=turnstiles_schema)
    write_to_console(df_messages, processing_time=window_duration)
      
    df_windowed = consumer.add_by_station(df_messages, window_duration, window_slide)
        
    write_to_storage(df_windowed, output_mode='append',processing_time=window_duration)
  
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
    parser.add_argument('--duration', required=False, help='window duration for aggregation 5 mins')        
    parser.add_argument('--slide', required=False, help='window slide 5 mins')        
    
    args = parser.parse_args()

    if (args.master is None):
        args.master = 'spark://localhost:7077'

    main_flow(args)

    print('end')

# Usage
# load spark shell
# spark-shell --packages org.apache.spark:spark-sql-kafka-0-10_2.12:your_spark_version

# run the app using spark-submit
# python3 program.py --topic mta-turnstile --group turnstile --client appTurnstile --config ~/.kafka/azure.properties
# spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2 program.py --topic mta-turnstile --group turnstile --client appTurnstile --config ~/.kafka/azure.properties

# export KAFKA_OPTS="java.security.auth.login.config=~/.kafka/azure.properties.jaas"

# spark-submit --conf spark.kafka.sasl.jaas.config=~/.kafka/azure.properties.jaas --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2 program.py --topic mta-turnstile --group turnstile --client appTurnstile --config ~/.kafka/azure.properties

# spark-shell --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2